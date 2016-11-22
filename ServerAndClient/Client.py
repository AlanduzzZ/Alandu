#!/usr/bin/python3.4
#-*- coding:utf-8 -*-

from socket import *

host = '10.10.2.75'
port = 20001
addr = (host, port)
respdata = b''

def SocketClient(data):
    Client = socket(AF_INET, SOCK_STREAM)
    try:
        Client.connect(addr)
    except ConnectionRefusedError:
        raise SystemExit(r'ConnectionRefusedError: Server(%s)Port(%s)未打开或连接被拒绝' % (host, port))
    except ConnectionResetError:
        raise SystemExit(r'ConnectionResetError: Server(%s)强制关闭连接' % host)
    else:
        if not data:
            raise SystemExit('The data is Empty')
        senddata = '%s\r\n' % data
        try:
            Client.sendall(senddata.encode())
            respdata = Client.recv(1024)
        except OSError:
            raise SystemExit(r'OSError: Client与Server(%s)Port(%s)的连接未建立' % (host, port))
            pass
        finally:
            Client.close()
    if not respdata:
        raise SystemExit(r'Server response is Empty !')
        pass
    else:
        return respdata.decode().strip()