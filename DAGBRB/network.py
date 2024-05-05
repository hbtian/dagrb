# -*- coding: utf8 -*-
import gevent
from gevent import monkey
monkey.patch_all()

from gevent.queue import Queue
from gevent.server import StreamServer
from gevent import Greenlet
from socket import error as SocketError
import socks
from os.path import expanduser
from optparse import OptionParser
from DAGBRB import initialSTATUS_LIST
from RBC import bcProcessParty,recvProcessParty,recvBatchProcessParty
from gevent.event import Event
import struct
import cProfile
IP_MAPPINGS=[]
IP_LIST=None
STATUS_LIST=None
BASE_PORT=30000

def prepareIPList(content):
    global IP_LIST, IP_MAPPINGS,BASE_PORT
    PORT=BASE_PORT
    IP_LIST = content.strip().split('\n')
    # 真实网络环境下的IP_MAPPINGS
    IP_MAPPINGS = [(host, BASE_PORT) for host in IP_LIST if host]
    # 单机网络环境下的IP_MAPPINGS
    # for host in IP_LIST:
    #     IP_MAPPINGS.append((host,PORT))
    #     PORT += 1
    print("prepareIPList is exec...")
    print("IP_LIST:",IP_LIST)
    print("IP_MAPPINGS",IP_MAPPINGS)

def prepareStatusList(content):
    global STATUS_LIST
    STATUS_LIST = content.strip().split('\n')
    print("prepareStatusList is exec...")
    print("STATUS_LIST:",STATUS_LIST)

def msgdecode(msg):
    msg=msg.decode().strip().replace('[', '').replace(']', '').split(',')
    for i in range(len(msg)):
        if type(msg[i]) == str:
            msg[i] = msg[i].replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('"', '')
        if type(msg[i]) == bytes:
            msg[i] = msg[i].decode()
    return msg

buffer = b''

def recvuntil(socket, msg):
    global buffer
    ret = b''
    while True:
        if msg in buffer:
            ret = buffer[:buffer.find(msg)]
            buffer = buffer[buffer.find(msg)+len(msg):]
            break
        part = socket.recv(65536)
        buffer += part
        if len(part) < 65536:
            break
    return ret

def goodread(f, length):
    ltmp = length
    buf = []
    while ltmp > 0:
        buf.append(f.read(ltmp))
        ltmp -= len(buf[-1])
    return b''.join(buf)

def listen_to_channel(port):
    q= Queue()
    def _handle(socket,adress):
        # msg = socket.recv(65536)

        # while True:
            # if msg:
            #     print("msg:",msg)
            #     # while b'+++' in msg:
            #     #     ret=msg[:msg.find(b'+++')]
            #     #     msg=msg[msg.find(b'+++')+len(b'+++'):]
            #     #     q.put(ret)
            #     q.put(msg)
            #     break
        f = socket.makefile(mode="rb")
        while True:
            msglength, = struct.unpack('<I', goodread(f, 4))
            line = goodread(f, msglength)
            q.put(line)

    server = StreamServer(('0.0.0.0', port), _handle)
    server.start()
    return q

def connect_to_channel(hostname, port,party):
    retry=True
    s = socks.socksocket()
    while retry:
      try:
        s = socks.socksocket()
        s.connect((hostname, port)) #连接在这里
        retry = False
      except Exception as e:
        print("error:",e)
        retry = True
        s.close()

    q = Queue()
    def _handle():
        while True:
            obj = q.get()
            content=str(obj).encode('utf8')
            try:
                # print("sended:",obj)
                # s.sendall((str(obj)+'+++').encode('utf8'))
                # print("content:",content)
                s.sendall(struct.pack('<I', len(content)) + content)
            except SocketError:
                print("!! [to %d] sending error",(hostname,port,party)) # 为什么这里会出错？

    gtemp = Greenlet(_handle)
    gtemp.start()
    return q

# def listener(receive):
#     while True:
#         msg=receive()
#         if msg:
#             # msg=msg.decode()
#             print("received:",msg)



def initialize_network(options):
    # myStatus=options.status
    myId=options.id
    N = len(IP_MAPPINGS) #N是总节点数
    initialSTATUS_LIST(STATUS_LIST)
    #实际网络的监听
    listenchannel=listen_to_channel(BASE_PORT)
    #单机网络的监听

    # listenchannel=listen_to_channel(30004)


    # glistening = Greenlet(listener, listenchannel.get)
    # glistening.start()

    print('listening...')

    #建立广播连接
    def makeBroadcast(i):
        chans = []
        for j in range(N):
            host, port = IP_MAPPINGS[j]
            chans.append(connect_to_channel(host, port, i)) #可以看到是有端口的，单机模式下可以通过不同的端口去模拟
        def _broadcast(v):
            for j in range(N):
                chans[j].put(v)  # from i to j send v
        def _send(j, v):
            chans[j].put((j, i, v))
        return _broadcast, _send   #返回广播通道、单播通道

    glist=[]
    gevent.sleep(10) # wait for set-up to be ready


    if True:  # We only test for once
        bcList = dict()
        sdList = dict()
        tList = []

        def _makeBroadcast(x):  # 发送方x
            bc, sd = makeBroadcast(x)
            bcList[x] = bc  # x的广播通道
            sdList[x] = sd  # x的单播通道

        tmp_t = Greenlet(_makeBroadcast, myId)  # 为每一个server建立一个 打开广播和单播通道 的协程
        tmp_t.start()
        tList.append(tmp_t)
        gevent.joinall(tList)

        bc = bcList[myId]
        sd = sdList[myId]

        recv = listenchannel.get
        #print("recv:",recv)
        ts = []
        if options.status == 0:
            # 目前没有status=0
            print()
            # th = Greenlet(clientparty, myId, recv, bc, sd)
            # th.start()
            # ts.append(th)
        elif options.status == 1:
            # 候选链节点，只监听，更新自己的本地交易池
            th = Greenlet(bcProcessParty, myId, recv, bc, sd,N)

            th.start()
            ts.append(th)
        else:
            # InitICTState(IP_LIST)
            print("enter")
            # 未批处理
            th = Greenlet(recvProcessParty, myId, recv, bc, sd,N)
            # 批处理
            # th = Greenlet(recvBatchProcessParty, myId, recv, bc, sd, N)
            th.start()
            ts.append(th)

        try:
            gevent.joinall(ts)
        except Exception as e:
            print(e)

    evt = Event()
    evt.wait()
    # glistening.join()


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-s", "--hosts", dest="hosts",help="Host list file", metavar="HOSTS", default="~/hosts")
    parser.add_option("-a", "--status", dest="status",help="client node or chain node 0-client node;1-chain node;2-active chain node",
                      metavar="A", type="int")
    # parser.add_option("-a", "--status", dest="status",help="client node or chain node 0-client node;1-chain node;2-active chain node",
    #                   metavar="A", type="int")
    parser.add_option("-i", "--id", dest="id",help="node id",metavar="I", type="int")

    (options, args) = parser.parse_args()
    print("options:",options," args:",args)
    prepareIPList(open(expanduser(options.hosts), 'r').read())
    prepareStatusList(open('status','r').read())
    #print(STATUS_LIST)
    # initialize_network(options)
    cProfile.runctx("initialize_network(options)", globals(), locals(), sort='cumulative')







