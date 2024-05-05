# -*- coding: utf8 -*-
import time

import gevent
import schedule
from ecdsa import SigningKey, VerifyingKey, NIST256p
import threading
import hashlib
from gevent import monkey

monkey.patch_all()
from threading import Lock
# import timeit #用于测试程序片段耗时
from gevent import Greenlet
from crypto import Logger
import sys
import random  # 用于项目中的各种随机操作
import queue
from collections import deque
import nodes_dict

# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
# from pyvis.network import Network
sys.stdout = Logger(stream=sys.stdout)

'''
全局变量
'''
initialResponse1 = "initialResponse1"
initialResponse2 = "initialResponse2"
L = 0
STATUS_LIST = []
id = {
    'c97f640adb7b07863fde5755967258375032f97f800903ed57295e5eab241047': 0,
    'c7f5a65b10fd9d040678527f1f82b5dff39ab889e609ea07fc054a24dfdc9f7e': 1,
    'e9e99a5a2060dbfb25923b343c5d8be485981245d5d48c099c0c4e7cd7f38f17': 2,
    'c0e4fef131d52b60afb0af27e172b43884d07489b359283f39b26ba26c95e8a0': 3,
    '5c09a82383334ea01b8a482d9a5ecd778edd848090bc150be86146a6456f91e3': 4,
    '8769ef5a22757494aa9c74da64e00e80af71f396a4c635f410cff881623e58e6': 5,
    '8b959bcced57913d76d72651e508c58ac942b5b0956222ccc92ab8ed7dfe5205': 6,
    '81d33345ee0509d1cccce83b20ec69af9afcaef4fc3e9db2f9dc0fd163f2ed47': 7,
    '019bde8bd74c489729e8d8779e9d5d60fe19ca2eb01408cdc55e1120fea46344': 8,
    '5dd0f5dc3f44328604999965e1d3a67982711e5f82e9f95a14c48205d5074eba': 9,
    '5fb0f2cb4f5b6685d1f655cae650dac90793d669d200c4b70a88b967d84c1f7d': 10,
    'c1baef31a2bcf7c178da4aa565ff7e4d16111384e05a7f36fd683089ae6d8c34': 11,
    'df396c1d19e94b73c8367c494db83de42f8c8f2dcb19a41607bc2598b3498d1f': 12,
    '4d6523cc9271af3baa1d5d398e6a404215c1842235afa368381538cb5dc0ca16': 13,
    '95c07aceb6fc84a6b7f68206e6c2b2d8de2cee579b207e6ec30482cc2f743896': 14,
    '5014452fae00889d8a340a54bc0a42ab24627854246f44906a4c64d015943d19': 15,
    '8370ce4f092ecccaf277919dce5a206c1bd244c75d7a14fcc9418fbf1442f81e': 16,
    '749aed32fc1f8155d7b9e6892519e36eae1cf416da3b25dcca7c53f51484e596': 17,
    '0b8093dd749feb27326e1b6b5be4243541b3eadaf3904e44a32b669f7613a72a': 18,
    '3ffdb0755607607ffe6685f22488017032592313d265a6d4fe680db3dd5891dc': 19,
    'af076f4bf835af8021b844952680bda595d5074885fb7160f6cbf6dc14d0b25e': 20,
    '926dd4164fcfcef74368f8e1c0646d08faa3c5ed21ef23c75be3346ac17e1a40': 21,
    'c8630e7ed6e36a75e0b8e1d0054c800328487dc730b5968fed0bc198fbe38eba': 22,
    '3db43bcf10be97542f10a91725424270179592e7029ac029175c400f043a79e9': 23,
    'a6cb1132990d5e6a4dec5d82a058ae194a793059980ae102f5b4e0a6b965cd2b': 24,
    '103de475fdf7b9448dcff8b85ce02d15b51c0fa6b5333d14d067ac4c85eb2bfa': 25,
    '335dc016857a78b3eb4855f488779c76b7f3008f2f455965f2401e6cefd3c396': 26,
    'b187a0a7c73ea7900dc3f848331e555f2b7bd1a4f0248298a94deccc23158c36': 27,
    '93ee8bdebdf9acc4cfca870b87114744318de065eb0ce8015361efd960fe8146': 28,
    '6086d4faba736754c3ee59dafdcc02fd2788ff406916365af4900d7b0a057060': 29,
    '4afc924c55004ebc82ea285f11792d7a43b19eb6cb8561d41322cc5b115f056c': 30,
    'c0402a868773ce7800ac067cb9feca6cd93aaab8d1a08e1707cf60f19ea9aee8': 31,
    '2f64ed526dcaba261ddf689f616f5f7958d0d5a27630c6f89ccb4cad2cb08d61': 32,
    '40a45badc0c00d4d57993f4b2000f413a330f03eabd6969d78b0627968f4d7db': 33,
    'c4b21d79810abda91bbb77e065139378f49338ec39cdd4ab1d2fc30845a77167': 34,
    '27ed9785b6a9961435e7be1fa36971478b3f816875829bad9234cc7925b738db': 35,
    '49b69bb73b4c1492b52551f4c9c9b0a7216c61b112aefe2e6dc13e3824fcd8fb': 36,
    'b88ee852aff32c370654e22e99d670321afc0bebd65a08e2dd28fba2b58875be': 37,
    'f66e5be445966ee1214f62303e483272c74bfe2949947356e20068a5a7b50b80': 38,
    '360b088c52766841daecdee0a5353341f219a744f51828f598c7a7e6a98f4ee7': 39,
    '02af2867c39a39dfdc1b38b0b1bd304edb7ee787c94ad1081a1f17678111cf1f': 40,
    'cfb4a07f182d37fb6ca736c5e110534e2dc0e9e830a08f7527f611f020ca9b2e': 41,
    '6d78a6de4f13e92b233dd1145447f3ffdb803eee7dc554917d73abdec01db1e8': 42,
    'dbc771ba5faf5d623a0af5042d614be3a2354f6c4e5d971e00c4e7d3453d87d0': 43,
    '5b22277656b660de19c2882410b3e1a0edbf4b166e672e7a3a85160a10eec191': 44,
    '9f57c46106f3478c47355d22f96a4abe8ba1df325061cba128fdfc17149dc7c2': 45,
    '2a6fd410e21308836071336e3479098bd1981f1c934c936f1c1332c57584f688': 46,
    '0f17d7fa0f46cd7a85cca8356b5e16f41e40a61b987c1c3f6872534b4084dd33': 47,
    'ed613747e66c1e2911472f842ce70258907bda395ea66273f1741dd848a6220a': 48,
    'caea5bd4ca93cd5b5af4d045d092ae1b28fe17c3113f6d4716000acb0b2bea02': 49,
    'ec0b98ccfc6abde9e59b775ffd26ea416feade8391d837cf50b4a422cf849e28': 50,
    '2f2d8dd335a1569955315f4f374fe7aecf864ff64758fcc80293e04c66de5786': 51,
    '56f6b841d534a0e4a48dcb407b3e25716812674e76fe09134045a94125e65053': 52,
    'fc209167b691fa3bd58a81ea5c14729e113d5f32f36d8f1dbf35bbba36dc02a1': 53,
    '2b7436007654df1aebc6b7b2bed5901ec4a6d5c4ab16e22ffc9f734d6c49e264': 54,
    '2faed8511784e756a715b45599ce8bffb2b60e5a5bae71f6bb39b6ca3936eea0': 55,
    '51e13cf5e579ca9867d97ca9c08780e205d7775efa9f8f7c975cb6f5c3729fb3': 56,
    'c78220b41b1ff097f56e4f5dde6e2f8588841c88d653f3ed64d69a6231271624': 57,
    '61f082372a848e2a37c1e7351d4a35d96d7b9089e0a8278cd3517a604c9473f7': 58,
    '83cd014912362be951bce3a4cd02fd024eda41f5f81f4a8fcccae84121bb4b12': 59,
    '4837dd3d7be9e7ea9a55c4c406ee3c5f511c67b9fb84a63cba27788f8626ff8b': 60,
    'bd1670306886e4d2c469ec8705742e66937e8a6b3c83ca783e02fab436c80be4': 61,
    'c8a18f89d8cfd42e631bf64e2d17b2e61304263c76f1df41ce492174dca29ebc': 62,
    'f341a6ca39597de03cf051ea215f95c175868956bb2325741f014f8f95039051': 63,
    'fa252cfcf353d9b08d7dc89539fd20ddf1f9bd95a42a3b47b74e8edaffe6ad9c': 64,
    '3ca5feb45dd41dd6ea19e17a7ce9e5381ac4edc4c19b533b8327cd258eef636e': 65,
    '27f7156b516bd4ee0a8a29bf6a4c57d2b8a9b437259f4aa40cbdf13afa2cb270': 66,
    '94f30129e6e50d1d9887e1f5e6569dadb4419bbf78633b5eda39c298f77b5592': 67,
    'ea7143ffc7c1c6176fa354b815aafd16f1befcefe8d9b6d7035d789945f48e1f': 68,
    'ef9816afb11649a5e461a1b6342277755987bfff8929de7653a9396608b424da': 69,
    '2ba61d7662f4c96f468e02d4f340c9b486aba7f92f80cdf2c06fdd8031e059a3': 70,
    '46df279ff5b1db104f26a6215db7a4d1973da6f2787b62ef77547ff9ed3ff5fc': 71,
    'ab1d17b8cf7c44361584415e511a3cb532ee261d927863f863ce84eb3c35f0d0': 72,
    'c53df66c9fc0c2418d9508714e009af7a99d4899f32e77f2d332a5cc848235bd': 73,
    '44e6459d729e9160eb6e45ebe7d7c29c59d555bb4559ae9735d9aa96c999bc65': 74,
    'c31a378409c8f80704f4ea87ccc02106a6337790bfcb3e8783a7779fddb6777b': 75,
    '33a715b5e977713a58a803cddc9773cc6f518857521ffd3bcf3340b66728cd3b': 76,
    'ff08a6e29f4628b886fa0d4e34739f7266cc16a83d53737faff602607cb89171': 77,
    'e4d317b0052ce653f26942d98e3e2e5bff846acfb63a33ce79b63d0a57356704': 78,
    '628feb9fc8c85dcb91fbcf272fbb962a76aa87aff991e08eda2760518cffdd28': 79,
    'f53352cc52e799ee84b79c502e64c89541b62cd660a158dafa6944fb617259a1': 80,
    'ac6f0a449db1ac87e3eca9ff3bdf2bbb50a4c757fdbe25deeb96eceb0f443ca8': 81,
    '1e059eb7223e5b939cc8d7d87ed88d92d00a650fc371573f3f8caeaf2222fb85': 82,
    '5b81d0c4bac54b70aba9ec9ed8d50051a2d6aad976f9869619e26101845a4b20': 83,
    '6d227827bcca17dab94f3ac41fb93972983d3e6b71d59aa6221ca4a128fd981d': 84,
    '4f6cef2eac68148f92fbb7a9d3460ff71d9fd347a9ca94561a2efdf58ace7468': 85,
    '3c522d8a4e3c83e1be74dad2881d305d7a403aff747ddfc000bd924186efe99e': 86,
    '7011b632ce826e7225c21339c9c97b200f4425add2c526b21d3c37ad9f7397bf': 87,
    'cdefe0d6bdd29f5457d4c2ab6e4ed71092daab010106d1d047930f035bb2e279': 88,
    'ea9ddbaaac15addfef6108c2419ed84631166092d591365eb6689359f5dc9320': 89,
    '2f5940a4583bf19b5915a98182fc31810ca25f92600395e708014453aabcdc56': 90,
    'd080599b401ab9b41164b73565f7dbcc1be70d66e8f52efe9b8626d3ad207525': 91,
}
# id=\
# {
#   '0e881efe6df27f52135deddc707c6fbf':0,
#   'f9307d6751b306666b6c3ea97cabe6a6':1,
#   'ddb4159867aecbaea3b9130098c3dfe6':2,
#   '0be783441c46557665b7ca9a55936067':3,
#   '72ecf41e3c3d855167ffcc541e54cc24':4,
#   'f6b11edb5266d02397b4a2e783184bc1':5,
#   'd66138ecb89c346e2c220219a6870fea':6,
#   '2a8c7a47068d20ff9da6d745a1455559':7,
#   '156cc37605b8e19e8dd3722784c70dd9':8,
#   '867d04696ff1c5ab286d24de40cc1fa2':9,
#   '185695bdc9b1135feb41e7627397c098':10,
#   '0adf9fedab02038d31a884386a44b444':11,
#   'aabd85b686cac287bbb98e57a6cdbf9d':12,
#   '12af68f2ba229ab46a0fed163e743a21':13,
#   'd84d2e2ee2bcc5a4e9eecd1e04198442':14,
#   '408983242cecd829c0148fba5c440db3':15,
#   '0e9c0e827562a84e75ef1d3b9d5510e5':16,
#   'ec7c0b3ff5db1a993c539b22d68f8905':17,
#   '9f5887c6f8e5da2afbfaf57cefa15f9b':18,
#   '902ed084a9569491d065d7bce7b93413':19,
#   '33cdf5cbd40ed39870d9e20dd7884767':20,
#   '4be0b2333e12ed772d4d85653f45b2b6':21,
#   '745977ad15b9524087cf7b4ec2214550':22,
#   '995ec3280e1f7d9c7dc821ca54071530':23,
#   '2711bd7327b65d4741be5ea4608c2a99':24,
#   '4df44b5bfa9f816c21be6594373622b6':25,
#   'c64a7e185dc0f0eb7e174b743f0dc667':26,
#   '9e528be1fadc430ff5963f817722d38f':27,
#   'ceb700cf4afeac6ea2ee62b2db29f7fb':28,
#   '81175df59e7efb14de4d40533f8036a6':29,
#   '4834fa44f42b2def12b4a6e494195cb3':30,
#   '201a3c7f60f933bdda5d8ab988bf3658':31,
#   '342ecfe004b22fa204138a6f34e5ea39':32,
#   'a654a5ff9a2edffc900d0e0c84197364':33,
#   '515669e9157d973e0d085dbe5b0cc37d':34,
#   'f057bd8e521f9ddb37155751c4c9976b':35,
#   '8892de79267d377c664ef2dbad559ca4':36,
#   'f588678b45f230d00492a4598a913af0':37,
#   'eed83c2e5dd5cd5fc3351059bb95c757':38,
#   'cb4dd1c879f6962797e261824687d590':39,
#   '201bc4363f1b9de81d0c0cdb095a794f':40,
#   '1407ea788de533abbb78c429e7913a04':41,
#   'ee1098dc4af439fc214189d2cb3a6d49':42,
#   'd63776dd596e51d8175b8be914751afe':43,
#   'a677e84722d3b2fcbb9669253a3329a3':44,
#   '5ee6f5ae13911abf453caad410dcd842':45,
#   '99745af83bdeae762c94a07d7a45a0a3':46,
#   '34d8f929c7ca1fa874e7178ebf1fd2b4':47,
#   '9613968565c8899da8c04f1bea37fdcd':48,
#   '3b18c01fce75a28bb363c18c481fc0e8':49,
#   'e2fc6b59d2879b95aaf0ff3349f8fd7f':50,
#   '8a0aed11fed16d03412f5665c0bb94de':51,
#   'add6751975c5f713f83d235b0dbd6a65':52,
#   '3870f15e7405323365a0d9a5026b8ad1':53,
#   'cbcc8b88842de9c9ddf9e4f34e0605a5':54,
#   '83c9b3a2e3d3863a14263eeec1524333':55,
#   'f0ea401d69e51a7dfae56edf61bbe9e3':56,
#   'b351d2f5051b74426e1c8013b085f243':57,
#   'd07792a6e2724ab6b7cb172583b3b8c2':58,
#   'a4b6b55418adcea487e8be8497bec0f9':59,
#   '83fe571a22a1cb43cabc4bdaad9bef0f':60,
#   '4983ac3fdfc78077c0ce377eef86d995':61,
#   'a4165f3e2428c71848a9f3c104e67be8':62,
#   '80229c18ebdbd8df45124679323c8074':63,
#   'a6444eea5f1684083c5bd8919c0ffe77':64,
#   'bb94901664bd07d0c775429be4dd82f4':65,
#   '4ea797074a6e2ba06a553e1519899364':66,
#   'b81a13474566c847f747323524656863':67,
#   '15dd0ca84013e856fbdce7ab0045e5bc':68,
#   '177c297dd9a511fe20fdb39f1eb79562':69,
#   'db203469efbf6bbb54e55e39391e950c':70,
#   '8391577aad3444aa6ded001d53ac08c5':71,
#   '5976db95e6308b80a07a8880215fa6bc':72,
#   '371ac287bd365bdf66bae67ea078038d':73,
#   '922fea363319d25135b7a9304c2d1b61':74,
#   '48bbcb14b1650f74536b190fbc784d16':75,
#   'd19f205b78a4cddc5bcc0696ff7f8d62':76,
#   'cb632f8e16725b36ea1e5ae850f09ceb':77,
#   'c3b66140e9e95921f6c75fc5bf00c5b5':78,
#   '046c766b12c8c18a973073472338ce4b':79,
#   'a371899e19a8ce2318e2771ae0b5957c':80,
#   '8ed8bffd8b8fc990db886e9dfbb8337c':81,
#   'edabc0fe882733bbe0d2ae1abcb67146':82,
#   '57b64c73c21ab430d17c2f7f03416cc3':83,
#   '83f39bc3e575addd8a604b9ee75088c9':84,
#   '3c1c93b35de5b89cdfabf8cafc9b2f4e':85,
#   '6ed97e4e23d486ee291d576e340cb0b3':86,
#   'adf3a45b0fae85445e4b002b94d6ad0a':87,
#   '12a4b12748d5c66311ddc53e6b18e6bf':88,
#   '90c492ac862e8cf0f25e86977e951738':89,
#   'd08a4bf645deda80f2347eb9ddad3ff3':90,
#   'fc0ed0d254ec841a35a2750981526562':91
# }

# id={
#     'c97f640adb7b07863fde5755967258375032f97f800903ed57295e5eab241047':0,
#     'c7f5a65b10fd9d040678527f1f82b5dff39ab889e609ea07fc054a24dfdc9f7e':1,
#     'e9e99a5a2060dbfb25923b343c5d8be485981245d5d48c099c0c4e7cd7f38f17':2,
#     'c0e4fef131d52b60afb0af27e172b43884d07489b359283f39b26ba26c95e8a0':3,
#     '5c09a82383334ea01b8a482d9a5ecd778edd848090bc150be86146a6456f91e3':4,
#     '8769ef5a22757494aa9c74da64e00e80af71f396a4c635f410cff881623e58e6':5,
#     '8b959bcced57913d76d72651e508c58ac942b5b0956222ccc92ab8ed7dfe5205':6,
#     '81d33345ee0509d1cccce83b20ec69af9afcaef4fc3e9db2f9dc0fd163f2ed47':7,
#     '019bde8bd74c489729e8d8779e9d5d60fe19ca2eb01408cdc55e1120fea46344':8,
#     '5dd0f5dc3f44328604999965e1d3a67982711e5f82e9f95a14c48205d5074eba':9,
#     '5fb0f2cb4f5b6685d1f655cae650dac90793d669d200c4b70a88b967d84c1f7d':10,
#     'c1baef31a2bcf7c178da4aa565ff7e4d16111384e05a7f36fd683089ae6d8c34':11,
#     'df396c1d19e94b73c8367c494db83de42f8c8f2dcb19a41607bc2598b3498d1f':12,
#     '4d6523cc9271af3baa1d5d398e6a404215c1842235afa368381538cb5dc0ca16':13,
#     '95c07aceb6fc84a6b7f68206e6c2b2d8de2cee579b207e6ec30482cc2f743896':14,
#     '5014452fae00889d8a340a54bc0a42ab24627854246f44906a4c64d015943d19':15
# }
times = 1


def initialSTATUS_LIST(s):
    print("exec initialSTATUS_LIST")
    global STATUS_LIST
    global L
    STATUS_LIST = s
    for i in STATUS_LIST:
        if i == '2':
            L = L + 1
    print("L:", L)
    print(STATUS_LIST)


def Gethash(msg):
    if type(msg) == str:
        return hashlib.sha256(bytes(msg, 'utf8')).hexdigest()
    if type(msg) == bytes:
        return hashlib.sha256(msg).hexdigest()
    else:
        msg = str(msg)
        return hashlib.sha256(bytes(msg, 'utf8')).hexdigest()


# 客户端/服务端
class process:
    def __init__(self, name, status, N, broadcast):
        skname = "./skandvk/" + name + "sk.pem"
        vkname = "./skandvk/" + name + "vk.pem"
        try:
            fp = open(skname, 'rb+')
            tline = fp.read()
            self.sk = SigningKey.from_pem(tline)
            fp.close()
        except:
            fp = open(skname, 'wb+')
            self.sk = SigningKey.generate(curve=NIST256p)
            fp.write(self.sk.to_pem())
            fp.close()
        try:
            fp = open(vkname, 'rb+')
            tline = fp.read()
            self.vk = VerifyingKey.from_pem(tline)
            fp.close()
        except:
            fp = open(vkname, 'wb+')
            self.vk = self.sk.get_verifying_key()
            fp.write(self.vk.to_pem())
            fp.close()

        self.status = status  # 用于RBC.py文件区分不同结点

        # 逻辑上的DAG
        self.DAG_nodes = {Gethash(str(initialResponse1)), Gethash(str(initialResponse2))}
        self.hashToResponse = {Gethash(str(initialResponse1)): initialResponse1,
                               Gethash(str(initialResponse2)): initialResponse2}
        self.hashToInitial = {}

        # 缓存池
        self.initial_pool = queue.Queue()
        self.response_pool = queue.Queue()
        self.syncRequest_pool = queue.Queue()
        self.buffer = deque()
        self.inbuffer = deque()
        self.y = 9
        # self.batchInbuffer = [] # 列表
        # self.batchInbuffer = deque() # 队列
        self.batchResponsePool = []
        # 结点id，通过nodes_dict.py取0、1、2、3...
        print("self.id=", Gethash(self.vk.to_pem()))
        self.id = id[Gethash(self.vk.to_pem())]  # 结点公钥用作ID值 但其实这里有点小错
        # 打包大小
        self.batchSize = 650
        self.m = 5
        for i in range(self.m):
            column0 = 1
            column1 = self.initialize_column1(self.batchSize)

            column2 = [Gethash(1), Gethash(1), Gethash(1)]
            column3 = self.id
            self.batchResponsePool.append([column0, column1, column2, column3])
        self.cur_row = 0  # cur_row<self.m
        self.cur_col = 0  # cur_col<self.batch_size
        self.batchInbuffer = deque()

        # 计算打包开销
        self.startTime = 0
        self.endTime = 0



        # 辅助选取引用的集合
        # not_referenced和already_referenced需要按照结点编号分组
        self.not_referenced = {}
        self.already_referenced = {}

        for index, value in enumerate(STATUS_LIST):
            if value == '2':
                self.not_referenced[index] = {Gethash(str(initialResponse1)), Gethash(str(initialResponse2))}
                self.already_referenced[index] = set()

        # 客户端与服务端的数量

        self.N = N  # 总进程数
        self.m = N - L  # 发送进程数量
        self.n = L  # 接收进程数量
        # 3t+1<n
        # t<(n-1)/3
        self.t_m = int((self.m - 1) / 3)  # 拜占庭客户端至多的数量
        self.t_n = int((self.n - 1) / 3)  # 拜占庭服务端至多的数量
        print(N,self.t_n)

        self.predecessors = {}  # 组成为{response:{直接前驱和间接前驱的结点id的字典，值为1}} 这里没有区分不同进程的直接引用与间接引用

        # 关于消息结点v的字典S_i
        self.S = {}  # 组成为{response51:{6:1,7:1},response61:{7:1,8:1}} 这里需要有区分不同进程的直接引用与间接引用
        # 关于消息结点v的response的字典
        self.initialToResponse = {}  # 组成为{initial1:{response51,response61}}
        # 已经接收的initial
        self.recvBatchInitialSet = set()
        self.recvInitialCount = 0
        self.recvInitialPool = set()
        self.recvBatchInitialCount = 0
        # 计算tps
        self.initialTime = 0
        self.broadcast = broadcast
        self.lastSecondCount = 0


    # 辅助函数
    def initialize_column1(self, batchSize):
        # 初始化column1数组
        column1_element = self.packInitial(000000000000000)  # 使用packInitial函数初始化一个示例元素
        column1 = [column1_element for _ in range(batchSize)]
        return column1

    # 定时器

    def checkInitialPerSeconds(self):
        global times
        print("每秒决定：",self.recvInitialCount - self.lastSecondCount,"字典大小：",
              len(self.S),"总决定消息的数量：",self.recvInitialCount,"从开始到现在平均决定：",self.recvInitialCount/times,"times:",times)
        times = times + 1
        self.lastSecondCount = self.recvInitialCount


        # print("每秒决定：", (self.recvBatchInitialCount - self.lastSecondCount) / self.batchSize, "个batch", "字典大小：",
        #       len(self.S), "总决定batch的数量：", self.recvBatchInitialCount / self.batchSize, "从开始到现在平均决定：",
        #       self.recvBatchInitialCount / (times*self.batchSize), "inbatchbuffer大小：", len(self.batchInbuffer),"times:",times)
        # times = times + 1
        # self.lastSecondCount = self.recvBatchInitialCount

    def scheduleTasks(self):
        schedule.every(1).seconds.do(self.checkInitialPerSeconds)
        def _listener():
            while True:
                schedule.run_pending()
                gevent.sleep(1)
        Greenlet(_listener).start()

    def _listen_buffer(self):
        def _listener():
            while True:
                '''
                未批处理处理buffer
                '''
                if len(self.buffer) >= 10:
                    # print("此时buffer的大小超过10了，需要将buffer中的消息全部进行同步！")
                    while len(self.buffer) > 0:
                        timestamp, response = self.buffer.popleft()
                        references = [str(x) for x in response[2].split(',')]
                        need = []
                        for ref in references:
                            if ref not in self.DAG_nodes:
                                need.append(ref)
                        need = ','.join(need)
                        syncRequest = self.packSyncRequest(need, response)
                        self.broadcast(syncRequest)
                '''
                未批处理inbuffer
                '''
                if len(self.inbuffer) >=self.y:
                    print("处理inbuffer")
                    for i in range(int(self.y/2)):
                        initial = self.inbuffer.popleft()
                        if self.recvInitialPool.__contains__(Gethash(str(initial))) == False:
                            response = self.packResponse(initial)
                            self.broadcast(response)
                '''
                批处理buffer
                '''
                # if len(self.buffer) >= 10:
                #     print("此时buffer的大小超过10了，需要将buffer中的消息全部进行同步！")
                #     while len(self.buffer) > 0:
                #         timestamp, response = self.buffer.popleft()
                #         # references = [str(x) for x in response[2].split(',')]
                #         references = response[2]
                #         need = []
                #         for ref in references:
                #             if ref not in self.DAG_nodes:
                #                 need.append(ref)
                #         need = ','.join(need)
                #         syncRequest = self.packSyncRequest(need, response)
                #         self.broadcast(syncRequest)

                '''
                 批处理batchInbuffer
                '''
                # 列表
                # if len(self.batchInbuffer) >= 9 * self.batchSize:
                #     print("看看是否inbuffer了？")
                #     batchInbuffer = self.batchInbuffer
                #     for i in range(len(batchInbuffer) / self.batchSize):
                #         batch_initials = random.sample(self.batchInbuffer, self.batchSize)
                #         response = self.packBatchResponse(batch_initials)
                #         self.broadcast(response)

                # 队列
                # if len(self.batchInbuffer) >= 9 * self.batchSize:
                #     for i in range(9):
                #         batch_initials = [None] * self.batchSize
                #         for i in range(self.batchSize):
                #             batch_initials[i] = self.batchInbuffer.popleft()
                #         response = self.packBatchResponse(batch_initials)
                #         self.broadcast(response)

                # 二维数组和队列
                # if len(self.batchInbuffer) >= 32:
                #     print("处理inbuffer了")
                #     for i in range(16):
                #         response = self.batchInbuffer.popleft() # 引用得重新选
                #         response = eval(response)
                #         ref = []
                #         keys_without_excluded = [key for key in self.not_referenced.keys() if key != self.id]
                #         random_key0 = random.choice(keys_without_excluded)
                #         if (len(self.not_referenced[random_key0]) >= 1):
                #             ref1 = random.sample(self.not_referenced[random_key0], 1)  # list
                #             # 如果选中的是两个初始节点，则需要全部更新；否则，只需要更新对应的节点编号的键值
                #             if ref1[0] == Gethash(str(initialResponse1)) or ref1[0] == Gethash(str(initialResponse2)):
                #                 for key, value in self.not_referenced.items():
                #                     value.difference_update(ref1)
                #                     self.already_referenced[key] = self.already_referenced[key] | set(ref1)
                #             else:
                #                 self.not_referenced[int(self.hashToResponse[ref1[0]][3])].difference_update(ref1)
                #                 self.already_referenced[int(self.hashToResponse[ref1[0]][3])] = self.already_referenced[
                #                                                                                     int(
                #                                                                                         self.hashToResponse[
                #                                                                                             ref1[0]][
                #                                                                                             3])] | set(
                #                     ref1)
                #             ref1 = ref1[0]
                #         else:
                #             ref1 = random.sample(self.already_referenced[random_key0], 1)  # list
                #             # print("ref2:", ref2)
                #             ref1 = ref1[0]
                #         random_key = random.choice(keys_without_excluded)
                #         if (len(self.not_referenced[random_key]) >= 1):
                #             ref2 = random.sample(self.not_referenced[random_key], 1)  # list
                #             # 如果选中的是两个初始结点，需要全部更新；否则，只需要更新对应的结点编号的键值
                #             if ref2[0] == Gethash(str(initialResponse1)) or ref2[0] == Gethash(str(initialResponse2)):
                #                 # 全部更新
                #                 for key, value in self.not_referenced.items():
                #                     value.difference_update(ref2)
                #                     self.already_referenced[key] = self.already_referenced[key] | set(ref2)
                #             else:
                #                 # 更新对应键值
                #                 self.not_referenced[int(self.hashToResponse[ref2[0]][3])].difference_update(ref2)
                #                 self.already_referenced[int(self.hashToResponse[ref2[0]][3])] = self.already_referenced[
                #                                                                                     int(
                #                                                                                         self.hashToResponse[
                #                                                                                             ref2[0]][
                #                                                                                             3])] | set(
                #                     ref2)
                #
                #             ref2 = ref2[0]
                #             ref.append(ref1)
                #             ref.append(ref2)
                #         else:
                #             # 需要避免在alreay中选取与ref1相同的消息
                #             ref2 = random.sample(self.already_referenced[random_key], 1)  # list
                #             # print("ref2:", ref2)
                #             ref2 = ref2[0]
                #             # ref2与ref1重复了则重新选
                #             while ref2 == ref1:
                #                 ref2 = random.sample(self.already_referenced[random_key], 1)
                #                 ref2 = ref2[0]
                #             ref.append(ref1)
                #             ref.append(ref2)
                #         # # 如果DAG图中是否有节点被引用次数大于t+1，如果有，那么就加上这个引用
                #         # # 检查是否大于等于t+1
                #         S = self.S
                #         for key, value in S.items():
                #             if len(value) >= self.t_n + 1:
                #                 if value.__contains__(self.id) == False:
                #                     if key not in ref:
                #                         ref.append(key)
                #                         break
                #
                #         response[2][0] = ref[0]
                #         response[2][1] = ref[1]
                #         if len(ref) == 3:
                #             response[2][2] = ref[2]
                #         response = "{}".format(self.batchResponsePool[self.cur_row])
                #         self.broadcast(response)
                gevent.sleep()
        Greenlet(_listener()).start()

    def packInitial(self, M):
        '''
        # initial_i = (0,v,i)
        :return: initial_i
        '''

        initial = []
        initial.append(0)  # 0:initial
        str_M = str(M)  # 5
        target_size = 253
        # target_size = 253 * 200 # batch
        for i in range(target_size):
            str_M += "a"
        initial.append(str_M)
        initial.append(self.id)  # i
        initial = "{}".format(initial)
        return initial

    def packResponse(self, initial):
        '''
        :param initial:
        # response_ij=(1,initial=(0,M,j),ref,i)
        :return:
        '''
        response = []
        response.append(1)  # 1: response
        response.append(initial)
        ref = []
        keys_without_excluded = [key for key in self.not_referenced.keys() if key != self.id]
        random_key0 = random.choice(keys_without_excluded)
        if (len(self.not_referenced[random_key0]) >= 1):
            ref1 = random.sample(self.not_referenced[random_key0], 1)  # list
            # 如果选中的是两个初始节点，则需要全部更新；否则，只需要更新对应的节点编号的键值
            if ref1[0] == Gethash(str(initialResponse1)) or ref1[0] == Gethash(str(initialResponse2)):
                for key, value in self.not_referenced.items():
                    value.difference_update(ref1)
                    self.already_referenced[key] = self.already_referenced[key] | set(ref1)
            else:
                self.not_referenced[int(self.hashToResponse[ref1[0]][3])].difference_update(ref1)
                self.already_referenced[int(self.hashToResponse[ref1[0]][3])] = self.already_referenced[int(
                    self.hashToResponse[ref1[0]][3])] | set(ref1)
            ref1 = ref1[0]
        else:
            ref1 = random.sample(self.already_referenced[random_key0], 1)  # list
            ref1 = ref1[0]
        random_key = random.choice(keys_without_excluded)
        if (len(self.not_referenced[random_key]) >= 1):
            ref2 = random.sample(self.not_referenced[random_key], 1)  # list
            # 如果选中的是两个初始结点，需要全部更新；否则，只需要更新对应的结点编号的键值
            if ref2[0] == Gethash(str(initialResponse1)) or ref2[0] == Gethash(str(initialResponse2)):
                # 全部更新
                for key, value in self.not_referenced.items():
                    value.difference_update(ref2)
                    self.already_referenced[key] = self.already_referenced[key] | set(ref2)
            else:
                # 更新对应键值
                self.not_referenced[int(self.hashToResponse[ref2[0]][3])].difference_update(ref2)
                self.already_referenced[int(self.hashToResponse[ref2[0]][3])] = self.already_referenced[int(
                    self.hashToResponse[ref2[0]][3])] | set(ref2)
            ref2 = ref2[0]
            ref.append(ref1)
            ref.append(ref2)
        else:
            # 需要避免在alreay中选取与ref1相同的消息
            ref2 = random.sample(self.already_referenced[random_key], 1)  # list
            ref2 = ref2[0]
            # ref2与ref1重复了则重新选
            while ref2 == ref1:
                ref2 = random.sample(self.already_referenced[random_key], 1)
                ref2 = ref2[0]
            ref.append(ref1)
            ref.append(ref2)

        # # 如果DAG图中有被引用次数达到t+1且还没有对这个关于值v的消息结点v有直接引用或间接引用,那么就加上这个引用
        # # 检查是否大于等于t+1
        S = self.S
        initialToResponse = self.initialToResponse
        for I, R in initialToResponse.items():
            votes = {}
            # 统计票数
            for r in R:
                votes = votes | S[r]
            # 大于等于t+1
            if len(votes) >= self.t_n + 1:
                # 如果本进程还没有直接引用或者间接引用关于值v的消息结点
                # 直接判断本进程的id在不在votes里面
                if votes.__contains__(self.id) == False:
                    refx = random.sample(R, 1)  # list
                    refx = refx[0]
                    if refx not in ref:
                        ref.append(refx)
                        break  # 目前最多就引用一次
        response.append(','.join(ref))
        response.append(self.id)
        response = "{}".format(response)
        return response

    def packBatchResponse(self, batchInitial):
        '''
        :param batchInitial:
        # response_ij=(1,batchInitial,ref,i)
        :return:
        '''
        response = []
        response.append(1)  # 1: response
        response.append(batchInitial)
        ref = []
        keys_without_excluded = [key for key in self.not_referenced.keys() if key != self.id]
        random_key0 = random.choice(keys_without_excluded)
        if (len(self.not_referenced[random_key0]) >= 1):
            ref1 = random.sample(self.not_referenced[random_key0], 1)  # list
            # 如果选中的是两个初始节点，则需要全部更新；否则，只需要更新对应的节点编号的键值
            if ref1[0] == Gethash(str(initialResponse1)) or ref1[0] == Gethash(str(initialResponse2)):
                for key, value in self.not_referenced.items():
                    value.difference_update(ref1)
                    self.already_referenced[key] = self.already_referenced[key] | set(ref1)
            else:
                self.not_referenced[int(self.hashToResponse[ref1[0]][3])].difference_update(ref1)
                self.already_referenced[int(self.hashToResponse[ref1[0]][3])] = self.already_referenced[int(
                    self.hashToResponse[ref1[0]][3])] | set(ref1)
            ref1 = ref1[0]
        else:
            ref1 = random.sample(self.already_referenced[random_key0], 1)  # list
            ref1 = ref1[0]
        random_key = random.choice(keys_without_excluded)
        if (len(self.not_referenced[random_key]) >= 1):
            ref2 = random.sample(self.not_referenced[random_key], 1)  # list
            # 如果选中的是两个初始结点，需要全部更新；否则，只需要更新对应的结点编号的键值
            if ref2[0] == Gethash(str(initialResponse1)) or ref2[0] == Gethash(str(initialResponse2)):
                # 全部更新
                for key, value in self.not_referenced.items():
                    value.difference_update(ref2)
                    self.already_referenced[key] = self.already_referenced[key] | set(ref2)
            else:
                # 更新对应键值
                self.not_referenced[int(self.hashToResponse[ref2[0]][3])].difference_update(ref2)
                self.already_referenced[int(self.hashToResponse[ref2[0]][3])] = self.already_referenced[int(
                    self.hashToResponse[ref2[0]][3])] | set(ref2)

            ref2 = ref2[0]
            ref.append(ref1)
            ref.append(ref2)
        else:
            # 需要避免在alreay中选取与ref1相同的消息
            ref2 = random.sample(self.already_referenced[random_key], 1)  # list
            # print("ref2:", ref2)
            ref2 = ref2[0]
            # ref2与ref1重复了则重新选
            while ref2 == ref1:
                ref2 = random.sample(self.already_referenced[random_key], 1)
                ref2 = ref2[0]
            ref.append(ref1)
            ref.append(ref2)

        # # 如果DAG图中是否有节点被引用次数大于t+1，如果有，那么就加上这个引用
        # # 检查是否大于等于t+1
        S = self.S
        for key, value in S.items():
            if len(value) >= self.t_n + 1:
                if value.__contains__(self.id) == False:
                    if key not in ref:
                        ref.append(key)
                        break
        response.append(','.join(ref))
        response.append(self.id)
        response = "{}".format(response)

        return response

    def packSyncRequest(self, need, response):
        '''

        :param response:
        syncRequest = [1,need=[ref1,ref2],response,id]
        :return:
        '''
        syncRequest = []
        syncRequest.append(2)  # syncRequest
        syncRequest.append(need)
        syncRequest.append(response)
        syncRequest.append(self.id)
        syncRequest = "{}".format(syncRequest)
        return syncRequest

    def dealInitial(self, pid, receive, broadcast, send):
        def check(initial):
            return True

        def _listener():
            while True:
                initial = receive()
                if check(initial):
                    '''
                    模拟恶意节点
                    '''
                    # r = random.SystemRandom().randrange(self.n-self.t_n)
                    # if(r==1):
                    #     response = self.packResponse(initial)
                    #     j=random.SystemRandom().randrange(self.n)
                    #     send(j,response)
                    #     print("恶意进程向进程",j,"转发了：",response)

                    r = random.SystemRandom().randrange(self.n - self.t_n)  # 增加了概率
                    if (r == 1):
                        # self.hadResponsedInitial.add(Gethash(str(initial)))
                        response = self.packResponse(initial)
                        broadcast(response)
                    else:
                        self.inbuffer.append(initial)

        Greenlet(_listener()).start()

    def dealBatchInitial(self, pid, receive, broadcast, send):
        def check(initial):
            return True

        def _listener():
            while True:
                initial = receive()
                if check(initial):
                    '''
                    批处理
                    '''
                    # 列表
                    # self.batchInbuffer.append(initial)
                    # batchInbuffer = self.batchInbuffer
                    # if len(batchInbuffer)>=self.batchSize:
                    #     r = random.SystemRandom().randrange(self.n-self.t_n)
                    #     if r == 1:
                    #         batch_initials = random.sample(self.batchInbuffer, self.batchSize)
                    #         for item in batch_initials:
                    #             self.batchInbuffer.remove(item)
                    #         response = self.packBatchResponse(batch_initials)
                    #         broadcast(response)
                    # 队列
                    # self.batchInbuffer.append(initial)
                    # if len(self.batchInbuffer)>=self.batchSize:
                    #     r = random.SystemRandom().randrange(self.n-self.t_n)
                    #     if r == 1 :
                    #         batch_initials = [None] * self.batchSize
                    #         for i in range(self.batchSize):
                    #             batch_initials[i] = self.batchInbuffer.popleft()
                    #         response = self.packBatchResponse(batch_initials)
                    #         broadcast(response)

                    # 填充initial

                    self.batchResponsePool[self.cur_row][1][self.cur_col] = initial
                    if self.cur_col == 0:
                        self.startTime = time.time()
                    # 填满了，以1/2t+1概率转发，但引用还没选
                    if self.cur_col == self.batchSize-1:
                        print("填了", self.cur_col+1, "的数据了,封装成了一个包，打包开销：",time.time()-self.startTime)
                        ref = []
                        keys_without_excluded = [key for key in self.not_referenced.keys() if key != self.id]
                        random_key0 = random.choice(keys_without_excluded)
                        if (len(self.not_referenced[random_key0]) >= 1):
                            ref1 = random.sample(self.not_referenced[random_key0], 1)  # list
                            # 如果选中的是两个初始节点，则需要全部更新；否则，只需要更新对应的节点编号的键值
                            if ref1[0] == Gethash(str(initialResponse1)) or ref1[0] == Gethash(str(initialResponse2)):
                                for key, value in self.not_referenced.items():
                                    value.difference_update(ref1)
                                    self.already_referenced[key] = self.already_referenced[key] | set(ref1)
                            else:
                                self.not_referenced[int(self.hashToResponse[ref1[0]][3])].difference_update(ref1)
                                self.already_referenced[int(self.hashToResponse[ref1[0]][3])] = self.already_referenced[
                                                                                                    int(
                                                                                                        self.hashToResponse[
                                                                                                            ref1[0]][
                                                                                                            3])] | set(
                                    ref1)
                            ref1 = ref1[0]
                        else:
                            ref1 = random.sample(self.already_referenced[random_key0], 1)  # list
                            # print("ref2:", ref2)
                            ref1 = ref1[0]
                        random_key = random.choice(keys_without_excluded)
                        if (len(self.not_referenced[random_key]) >= 1):
                            ref2 = random.sample(self.not_referenced[random_key], 1)  # list
                            # 如果选中的是两个初始结点，需要全部更新；否则，只需要更新对应的结点编号的键值
                            if ref2[0] == Gethash(str(initialResponse1)) or ref2[0] == Gethash(str(initialResponse2)):
                                # 全部更新
                                for key, value in self.not_referenced.items():
                                    value.difference_update(ref2)
                                    self.already_referenced[key] = self.already_referenced[key] | set(ref2)
                            else:
                                # 更新对应键值
                                self.not_referenced[int(self.hashToResponse[ref2[0]][3])].difference_update(ref2)
                                self.already_referenced[int(self.hashToResponse[ref2[0]][3])] = self.already_referenced[
                                                                                                    int(
                                                                                                        self.hashToResponse[
                                                                                                            ref2[0]][
                                                                                                            3])] | set(
                                    ref2)

                            ref2 = ref2[0]
                            ref.append(ref1)
                            ref.append(ref2)
                        else:
                            # 需要避免在alreay中选取与ref1相同的消息
                            ref2 = random.sample(self.already_referenced[random_key], 1)  # list
                            # print("ref2:", ref2)
                            ref2 = ref2[0]
                            # ref2与ref1重复了则重新选
                            while ref2 == ref1:
                                ref2 = random.sample(self.already_referenced[random_key], 1)
                                ref2 = ref2[0]
                            ref.append(ref1)
                            ref.append(ref2)

                        # # 如果DAG图中是否有节点被引用次数大于t+1，如果有，那么就加上这个引用
                        # # 检查是否大于等于t+1
                        S = self.S
                        for key, value in S.items():
                            if len(value) >= self.t_n + 1:
                                if value.__contains__(self.id) == False:
                                    if key not in ref:
                                        ref.append(key)
                                        break

                        self.batchResponsePool[self.cur_row][2][0] = ref[0]
                        self.batchResponsePool[self.cur_row][2][1] = ref[1]
                        if len(ref) == 3:
                            self.batchResponsePool[self.cur_row][2][2] = ref[2]

                        r = random.SystemRandom().randrange(self.n) # 调整概率试试
                        response = "{}".format(self.batchResponsePool[self.cur_row])
                        if r == 1:
                            self.broadcast(response)
                            gevent.sleep()
                        else:
                            self.batchInbuffer.append(response)  # 队列append O(1)
                        #sleep加在这，直接没打包，也没发消息
                    self.cur_row = (self.cur_row + 1) % self.m
                    self.cur_col = (self.cur_col + 1) % self.batchSize

        Greenlet(_listener()).start()

    def addToDAG(self, response, broadcast):
        if Gethash(str(response)) in self.DAG_nodes:
            return
        initial = response[1]
        response_id = response[3]
        ref = [str(x) for x in response[2].split(',')]
        self.hashToInitial[Gethash(str(initial))] = initial
        # 逻辑的DAG
        self.DAG_nodes.add(Gethash(str(response)))
        self.hashToResponse[Gethash(str(response))] = response
        self.not_referenced[response_id].add(Gethash(str(response)))
        for r in ref:
            if r == Gethash(str(initialResponse1)) or r == Gethash(str(initialResponse2)):
                for key, value in self.not_referenced.items():
                    a = []
                    a.append(r)
                    value.difference_update(a)
                    self.already_referenced[key] = self.already_referenced[key] | set(a)
            else:
                a = []
                a.append(r)
                self.not_referenced[self.hashToResponse[r][3]].difference_update(a)
                self.already_referenced[self.hashToResponse[r][3]] = self.already_referenced[
                                                                         self.hashToResponse[r][3]] | set(a)

        # 把initial相关的response整理到一起
        if self.initialToResponse.__contains__(Gethash(str(initial))):
            self.initialToResponse[Gethash(str(initial))].add(Gethash(str(response)))
        else:
            self.initialToResponse[Gethash(str(initial))] = set()
            self.initialToResponse[Gethash(str(initial))].add(Gethash(str(response)))

        self.predecessors[Gethash(str(response))] = {}
        self.S[Gethash(str(response))] = {response_id: 1}
        new_predecessors = {}  # 遍历字典的时候字典不能有增加或者删除
        for key, value in self.predecessors.items():
            for i in ref:
                if i == key:  # 直接引用
                    new_predecessors[key] = value
                    new_predecessors[key][Gethash(str(response))] = 1
                    # 如果是直接引用，当前字典S中，response的id不等于key的id，也不在value里面，那么就可以说明当前新加入的response是对key的不同进程的引用
                    if response_id != self.hashToResponse[key][3] and self.S[key].__contains__(response_id) == False:
                        self.S[key][response_id] = 1
                elif value.__contains__(i):  # 间接引用
                    new_predecessors[key] = value
                    new_predecessors[key][Gethash(str(response))] = 1
                    # 如果是间接引用，当前字典S中，response的id不等于key的id，也不在value里面，那么就可以说明当前新加入的response是对key的不同进程的引用
                    if response_id != self.hashToResponse[key][3] and self.S[key].__contains__(response_id) == False:
                        self.S[key][response_id] = 1
        self.predecessors.update(new_predecessors)

        # 检查是否大于2t+1
        S = self.S
        initialToReponse = self.initialToResponse
        # 创建一个要删除的键的列表
        keys_to_remove = []
        for I, R in initialToReponse.items():
            votes = {}
            # 统计票数
            for r in R:
                votes = votes | S[r]
            # 大于2t+1(需要通过集合S统计"不同服务端")
            if len(votes) >= 2 * self.t_n + 1:
                # 决定
                # 删除字典S的response
                if self.recvInitialPool.__contains__(I) == False:
                    self.recvInitialCount = self.recvInitialCount + 1
                    self.recvInitialPool.add(I)
                for delr in R:
                    self.predecessors.pop(delr)  # 前驱字典删除关于v的response
                    self.S.pop(delr)  # 字典S删除关于v的response
                # 删除initialToResponse的initial
                keys_to_remove.append(I)
        for key in keys_to_remove:
            self.initialToResponse.pop(key)
            self.hashToInitial.pop(key)


    def addBatchToDAG(self, response, broadcast):
        if Gethash(str(response)) in self.DAG_nodes:
            return
        initial = response[1]
        response_id = response[3]
        ref = response[2]

        self.hashToInitial[Gethash(str(initial))] = initial

        # 逻辑的DAG
        self.DAG_nodes.add(Gethash(str(response)))
        self.hashToResponse[Gethash(str(response))] = response
        self.not_referenced[response_id].add(Gethash(str(response)))
        for r in ref:
            if r != Gethash(1):
                if r == Gethash(str(initialResponse1)) or r == Gethash(str(initialResponse2)):
                    for key, value in self.not_referenced.items():
                        a = []
                        a.append(r)
                        value.difference_update(a)
                        self.already_referenced[key] = self.already_referenced[key] | set(a)
                else:
                    a = []
                    a.append(r)
                    self.not_referenced[self.hashToResponse[r][3]].difference_update(a)
                    self.already_referenced[self.hashToResponse[r][3]] = self.already_referenced[
                                                                             self.hashToResponse[r][3]] | set(a)

        self.predecessors[Gethash(str(response))] = {}
        self.S[Gethash(str(response))] = {response_id: 1}
        new_predecessors = {}  # 遍历字典的时候字典不能有增加或者删除
        for key, value in self.predecessors.items():
            for i in ref:
                if i != Gethash(1):
                    if i == key:  # 直接引用
                        new_predecessors[key] = value
                        new_predecessors[key][Gethash(str(response))] = 1
                        # 如果是直接引用，当前字典S中，response的id不等于key的id，也不在value里面，那么就可以说明当前新加入的response是对key的不同进程的引用
                        if response_id != self.hashToResponse[key][3] and self.S[key].__contains__(
                                response_id) == False:
                            self.S[key][response_id] = 1
                    elif value.__contains__(i):  # 间接引用
                        new_predecessors[key] = value
                        new_predecessors[key][Gethash(str(response))] = 1
                        # 如果是间接引用，当前字典S中，response的id不等于key的id，也不在value里面，那么就可以说明当前新加入的response是对key的不同进程的引用
                        if response_id != self.hashToResponse[key][3] and self.S[key].__contains__(
                                response_id) == False:
                            self.S[key][response_id] = 1
        self.predecessors.update(new_predecessors)

        # 检查是否大于2t+1

        S = self.S
        keys_to_remove = []
        for key, value in S.items():
            if len(value) >= 2 * self.t_n + 1:
                # 决定
                self.recvBatchInitialCount = self.recvBatchInitialCount + self.batchSize
                keys_to_remove.append(key)

        for key in keys_to_remove:
            # 删除字典S
            self.predecessors.pop(key)
            self.S.pop(key)

    def dealResponse(self, pid, receive, broadcast, send):
        def check(response):
            # 检查引用在不在DAG里面
            ref = [str(x) for x in response[2].split(',')]
            for i in ref:
                if i not in self.DAG_nodes:
                    return False
            return True

        def _listener():
            while True:
                response = receive()
                # 收到response后，不管是否入图，都把response的initial从inbuffer移除
                initial = response[1]
                for i in range(len(self.inbuffer)):
                    item = self.inbuffer.pop()
                    if str(item) == str(initial):
                        # print("收到response里面的initial了，删除inbuffer里面对应的initial")
                        continue
                    else:
                        self.inbuffer.append(item)
                if check(response):
                    self.addToDAG(response, broadcast)
                    # 然后检查buffer,是否有消息结点满足入图条件
                    sz = len(self.buffer)
                    for i in range(sz):
                        timestamp, buffer_response = self.buffer.popleft()
                        if check(buffer_response):  # 新加入的结点能够让buffer的结点满足入图条件
                            self.addToDAG(buffer_response, broadcast)
                        else:  # 未满足入图条件
                            self.buffer.append((timestamp, buffer_response))
                else:
                    self.buffer.append((time.time(), response))

        Greenlet(_listener).start()

    def dealBatchResponse(self, pid, receive, broadcast, send):
        def check(response):

            # 检查引用在不在DAG里面
            ref = response[2]
            for i in ref:
                if i not in self.DAG_nodes and i != Gethash(1):
                    return False
            return True

        def _listener():
            while True:
                response = receive()
                #队列/列表
                # 收到response后，不管是否入图，都把response的batchInitial移除
                # batchInitial = response[1]
                # for initial in batchInitial:
                #     if initial in self.batchInbuffer:
                #         self.batchInbuffer.remove(initial)
                # 数组
                # 这里的response的id都是其他客户端发过来的，所以你要把id改成自己的id
                to_remove = []
                for r in self.batchInbuffer:
                    #print("response[1]:",response[1])
                    #print("r[1]:",eval(r)[1])
                    if response[1] == eval(r)[1]:
                        #print("不删一下？")
                        to_remove.append(r)
                for i in to_remove:
                    self.batchInbuffer.remove(i)
                if check(response):
                    self.addBatchToDAG(response, broadcast)
                    # 然后检查buffer,是否有消息结点满足入图条件
                    sz = len(self.buffer)
                    for i in range(sz):
                        timestamp, buffer_response = self.buffer.popleft()
                        if check(buffer_response):  # 新加入的结点能够让buffer的结点满足入图条件
                            self.addBatchToDAG(buffer_response, broadcast)
                        else:  # 未满足入图条件
                            self.buffer.append((timestamp, buffer_response))
                else:
                    self.buffer.append((time.time(), response))

        Greenlet(_listener).start()

    def dealSyncRequest(self, pid, receive, broadcast, send):
        def check(syncRequest):
            return True
        def _listener():
            while True:
                syncRequest = receive()
                if check(syncRequest):
                    ref = [str(x) for x in syncRequest[1].split(',')]
                    for i in ref:
                        if i in self.DAG_nodes:
                            response = self.hashToResponse[i]  # 发引用
                            send(syncRequest[3], response)
                    send(syncRequest[3], syncRequest[2])  # 发响应消息

        Greenlet(_listener).start()
