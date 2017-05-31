# -*- coding:utf-8 -*-
from ranking.AdsRankingServiceHandler import *
from ranking import AdsRankingService
from ranking.MyTBinaryProtocol import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.server import TServer
import sys
import threading


if __name__ == '__main__':
    handler = AdsRankingServiceHandler()
    processor = AdsRankingService.Processor(handler)
    transport = TSocket.TServerSocket(host='127.0.0.1', port=9095)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = MyTBinaryProtocolFactory()

    server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

    # 函数不能有括号，否则不是并行的
    t1 = threading.Thread(target=handler.start)
    t1.start()

    t2 = threading.Thread(target=server.serve)
    print "Ranking server: ready to start."
    t2.start()

    while True:
        try:
            word = raw_input()
            if word == 'stop':
                handler.stop()
                sys.exit(0)
        except Exception as e:
            print(repr(e))


