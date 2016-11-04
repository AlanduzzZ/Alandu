#!/usr/local/python3/bin/python3
#-*- coding:utf-8 -*-

from socket import *

host = '127.0.0.1'
port = 20001
addr = (host, port)
Client = socket(AF_INET, SOCK_STREAM)
try:
    Client.connect(addr)
except ConnectionRefusedError:
    print('ConnectionRefusedError: Server(%s)端口(%s)未打开或连接被拒绝' % (host, port))
except ConnectionResetError:
    print('ConnectionResetError: Server(%s)强制关闭连接' % host)

while True:
    data = input('Please input the data :')
    if not data or data==r'exit' or data==r'EXIT':
        break
    senddata = '%s\n' % data
    print(r'Your senddata is %s' % senddata.strip())
    try:
        Client.sendall(senddata.encode())
        respdata = Client.recv(1024)
    except OSError:
        print('OSError: Client与Server(%s)端口(%s)的连接未建立' % (host, port))
        respdata = b''
        pass
    if not respdata:
        print(r'Server response is Empty !')
        pass
    else:
        print(r'Your respdata is %s' % respdata.decode().strip())
Client.close()