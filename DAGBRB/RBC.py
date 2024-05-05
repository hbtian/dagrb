# -*- coding: utf8 -*-
import os
import time
import gevent
from gevent.pool import Pool
import schedule


from DAGBRB import process
from gevent import Greenlet
import functools

count = 0

def broadcastInitial(bcProcess,broadcast,tps):
    global count
    print(time.time(),count)
    for i in range(tps):
        initial = bcProcess.packInitial(count)
        count = count + 1
        broadcast(initial)
        gevent.sleep()
def bcProcessParty(pid,receive,broadcast,send,N):
    bcProcess = process('chain node ' + str(pid + 1),1,N,broadcast)
    tps = 5
    schedule.every(1).seconds.do(functools.partial(broadcastInitial,bcProcess,broadcast,tps))
    for i in range(120):
        schedule.run_pending()
        time.sleep(1)

def recvProcessParty(pid,receive,broadcast,send,N):
    recvProcess = process('chain node '+str(pid+1),2,N,broadcast)
    Greenlet(recvProcess._listen_buffer).start()
    Greenlet(recvProcess.scheduleTasks).start() # 开启定时任务
    def listener():
        while True:
            message = eval(receive())
            #print("Message:",message)
            if(len(message)==3 and len(str(message[2]))>5):
                # 说明这个是单播信息(i,j,message)
                message=eval(str(message[2]))
                #print("listener target from send",message)
            if int(message[0]) == 0:
                #print("add initial_pool")
                Greenlet(recvProcess.initial_pool.put,message).start()
            elif int(message[0]) == 1:
                #print("add response_pool")
                Greenlet(recvProcess.response_pool.put,message).start()
            elif int(message[0]) == 2:
                #print("add syncRequest_pool")
                Greenlet(recvProcess.syncRequest_pool.put,message).start()
            else:
                print("error type:",int(message[0]))
            Greenlet(recvProcess.dealInitial,pid,recvProcess.initial_pool.get,broadcast,send).start()
            Greenlet(recvProcess.dealResponse,pid,recvProcess.response_pool.get,broadcast,send).start()
            Greenlet(recvProcess.dealSyncRequest,pid,recvProcess.syncRequest_pool.get,broadcast,send).start()
    Greenlet(listener).start()


def recvBatchProcessParty(pid,receive,broadcast,send,N):
    recvProcess = process('chain node ' + str(pid + 1), 2, N, broadcast)
    Greenlet(recvProcess._listen_buffer).start()
    Greenlet(recvProcess.scheduleTasks).start()
    def listener():
        while True:
            message = eval(receive())
            #print(message)
            if (len(message) == 3 and len(str(message[2])) > 5):
                # 说明这个是单播信息(i,j,message)
                message = eval(str(message[2]))
                # print("listener target from send",message)
            if int(message[0]) == 0:
                # print("add initial_pool")
                Greenlet(recvProcess.initial_pool.put, message).start()
            elif int(message[0]) == 1:
                # print("add response_pool")
                Greenlet(recvProcess.response_pool.put, message).start()
            elif int(message[0]) == 2:
                # print("add syncRequest_pool")
                Greenlet(recvProcess.syncRequest_pool.put, message).start()
            else:
                print("error type:", int(message[0]))
            Greenlet(recvProcess.dealBatchInitial, pid, recvProcess.initial_pool.get, broadcast, send).start()
            Greenlet(recvProcess.dealBatchResponse, pid, recvProcess.response_pool.get, broadcast, send).start()
            Greenlet(recvProcess.dealSyncRequest, pid, recvProcess.syncRequest_pool.get, broadcast, send).start()

    Greenlet(listener).start()