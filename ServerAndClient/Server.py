#!/usr/local/python3/bin/python3
#-*- coding:utf-8 -*-

import traceback
from socketserver import StreamRequestHandler
from socketserver import ThreadingTCPServer

class MyServer(StreamRequestHandler):
    def handle(self):
        isTrue = True
        while isTrue:
            try:
                print(r'Client %s 已连接......' % self.client_address[0])
                reqdata = self.rfile.readline().decode().strip()
                print(r'Client IP is: %s ,data is %s, type is %s' % (self.client_address, reqdata, type(reqdata)))
                senddata = reqdata.upper() + '\r\n'
                self.wfile.write(senddata.encode())
            except ConnectionAbortedError:
                print(r'ConnectionAbortedError: Client %s 已经关闭连接' % self.client_address[0])
            except ConnectionResetError:
                print(r'ConnectionResetError: Client %s 强制关闭连接' % self.client_address[0])
            except Exception:
                traceback.print_exc()
                print(r'Client %s 已关闭连接!' % self.client_address[0])
            finally:
                print(r'Client %s 已关闭连接!' % self.client_address[0])
                isTrue = False

class MyThreadingTCPServer(ThreadingTCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    host = '0.0.0.0'
    port = 20001
    addr = (host, port)
    server = MyThreadingTCPServer(addr, MyServer)
    server.serve_forever()