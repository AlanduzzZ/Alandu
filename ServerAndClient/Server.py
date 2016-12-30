#!/usr/local/python3/bin/python3.5
#-*- coding:utf-8 -*-

import traceback
from socketserver import StreamRequestHandler
from socketserver import ThreadingTCPServer
import sys
from UserManage.addUser import *
import json
import Mylogger


class MyServer(StreamRequestHandler):

    def handle(self):
        isTrue = True
        while isTrue:
            try:
                Mylogger.UserManagelog.info('Client %s 已连接......\n' % self.client_address[0])
                reqdata = self.rfile.readline().decode().strip()
                reqdata = json.loads(reqdata)
                Mylogger.UserManagelog.info('Client IP is: %s ,data is %s, type is %s\n' % (self.client_address, reqdata, type(reqdata)))
                if reqdata['tag'] in ['getUserInfo', 'addRemoteUser']:
                    if reqdata['tag'] == 'getUserInfo':
                        senddata = UserToolsApp.getUserinfo(reqdata['username'])
                    elif reqdata['tag'] == 'addRemoteUser':
                        __RLocaluseradd = RLocaluseradd(reqdata['username'], reqdata['sudo'], reqdata['key'])
                        senddata = __RLocaluseradd.userAdd()
                    else:
                        senddata = ''
                else:
                    Mylogger.UserManagelog.critical('The tag is Error')
                    raise SystemExit('The tag is Error')
                senddata_json = json.dumps(senddata) + '\r\n'
                self.wfile.write(senddata_json.encode())
                Mylogger.UserManagelog.debug(senddata_json)
            except ConnectionAbortedError:
                Mylogger.UserManagelog.critical('ConnectionAbortedError: Client %s 异常关闭连接\n' % self.client_address[0])
                raise 'ConnectionAbortedError: Client %s 异常关闭连接\n' % self.client_address[0]
            except ConnectionResetError:
                Mylogger.UserManagelog.critical('ConnectionResetError: Client %s 强制关闭连接\n' % self.client_address[0])
                raise 'ConnectionResetError: Client %s 强制关闭连接\n' % self.client_address[0]
            except Exception:
                Mylogger.UserManagelog.critical(traceback.print_exc())
                Mylogger.UserManagelog.critical('Client %s 异常关闭连接!\n' % self.client_address[0])
                raise 'Client %s 异常闭连接!\n' % self.client_address[0]
            finally:
                Mylogger.UserManagelog.info('Client %s 已关闭连接!\n' % self.client_address[0])
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