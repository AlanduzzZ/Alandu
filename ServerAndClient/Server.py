#!/usr/bin/python3.4
#-*- coding:utf-8 -*-

import traceback
from socketserver import StreamRequestHandler
from socketserver import ThreadingTCPServer
import sys

class MyServer(StreamRequestHandler):
    def handle(self):
        isTrue = True
        while isTrue:
            try:
                sys.stdout.write('Client %s 已连接......\n' % self.client_address[0])
                sys.stdout.flush()
                reqdata = self.rfile.readline().decode().strip()
                sys.stdout.write('Client IP is: %s ,data is %s, type is %s\n' % (self.client_address, reqdata, type(reqdata)))
                senddata = reqdata.upper() + '\r\n'
                self.wfile.write(senddata.encode())
            except ConnectionAbortedError:
                sys.stdout.write('ConnectionAbortedError: Client %s 已经关闭连接\n' % self.client_address[0])
            except ConnectionResetError:
                sys.stdout.write('ConnectionResetError: Client %s 强制关闭连接\n' % self.client_address[0])
            except Exception:
                traceback.print_exc()
                sys.stdout.write('Client %s 已关闭连接!\n' % self.client_address[0])
            finally:
                sys.stdout.write('Client %s 已关闭连接!\n' % self.client_address[0])
                sys.stdout.flush()
                isTrue = False

class MyThreadingTCPServer(ThreadingTCPServer):
    allow_reuse_address = True

"""
if __name__ == "__main__":
    host = '0.0.0.0'
    port = 20001
    addr = (host, port)
    server = MyThreadingTCPServer(addr, MyServer)
    server.serve_forever()
"""