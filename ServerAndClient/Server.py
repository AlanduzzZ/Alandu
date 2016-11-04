#!/usr/local/python3/bin/python3
#-*- coding:utf-8 -*-

import traceback
from socketserver import StreamRequestHandler
from socketserver import ThreadingTCPServer

class MyServer(StreamRequestHandler):
    def handle(self):
#        allow_reuse_address = True
        while True:
            try:
                reqdata = self.rfile.readline().strip().decode()
                print('Client IP is: %s ,data is %s, type is %s' % (self.client_address, reqdata, type(reqdata)))
#                senddata = 'Your data is',reqdata
                senddata = reqdata.upper() +  '\r\n'
                self.wfile.write(senddata.encode())
            except ConnectionAbortedError:
                print('ConnectionAbortedError: Client %s 已经关闭连接' % self.client_address[0])
                break
            except ConnectionResetError:
                print('ConnectionResetError: Client %s 强制关闭连接' % self.client_address[0])
                break
            except Exception:
                traceback.print_exc()
                break

class MyThreadingTCPServer(ThreadingTCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    host = '0.0.0.0'
    port = 20001
    addr = (host, port)
    server = MyThreadingTCPServer(addr, MyServer)
    server.serve_forever()