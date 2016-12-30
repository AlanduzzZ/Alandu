#!/usr/local/python3/bin/python3.5
#-*- coding:utf-8 -*-

from socket import *
import json
import Mylogger

host = '10.10.2.75'
port = 20001
addr = (host, port)
respdata = b''

def SocketClient(data):
    Client = socket(AF_INET, SOCK_STREAM)
    try:
        Mylogger.UserManagelog.info('Connect host {} port {} start...'.format(host, port))
        Client.connect(addr)
    except ConnectionRefusedError:
        Mylogger.UserManagelog.critical('ConnectionRefusedError: Server({})Port({})未打开或连接被拒绝'.format(host, port))
        raise SystemExit(r'ConnectionRefusedError: Server({})Port({})未打开或连接被拒绝'.format(host, port))
    except ConnectionResetError:
        Mylogger.UserManagelog.critical('ConnectionResetError: Server({})强制关闭连接'.format(host))
        raise SystemExit(r'ConnectionResetError: Server({})强制关闭连接'.format(host))
    else:
        if not data:
            Mylogger.UserManagelog.critical('The data is Empty')
            raise SystemExit('The data is Empty')
        json_data = json.dumps(data)
        senddata = '{}\r\n'.format(json_data)
        Mylogger.UserManagelog.debug(senddata)
        try:
            Client.sendall(senddata.encode())
            respdata = Client.recv(1024)
            respdata_de = respdata.decode().strip()
            respdata_json = json.loads(respdata_de)
        except OSError:
            Mylogger.UserManagelog.critical('OSError: Client与Server({})Port({})的连接未建立'.format(host, port))
            raise SystemExit(r'OSError: Client与Server({})Port({})的连接未建立'.format(host, port))
    finally:
        Mylogger.UserManagelog.info('Connect host {} port {} close...'.format(host, port))
        Client.close()
    if not respdata_json:
        Mylogger.UserManagelog.critical('Server response is Empty !')
        raise SystemExit(r'Server response is Empty !')
        pass
    else:
        Mylogger.UserManagelog.debug(respdata_json)
        return respdata_json