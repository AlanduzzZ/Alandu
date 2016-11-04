#!/usr/local/python3/bin/python3
#-*- coding:utf-8 -*-

from socket import *

host = '127.0.0.1'
port = 20001
addr = (host, port)
Client = socket(AF_INET, SOCK_STREAM)
try:
    print(r'已连接Server(%s)Port(%s)......' % (host,port))
    Client.connect(addr)
except ConnectionRefusedError:
    print(r'ConnectionRefusedError: Server(%s)Port(%s)未打开或连接被拒绝' % (host, port))
except ConnectionResetError:
    print(r'ConnectionResetError: Server(%s)强制关闭连接' % host)
else:
    isTrue = True
    while isTrue:
        data = input(r'Please input the data :')
        if not data or data==r'exit' or data==r'EXIT':
            break
        senddata = '%s\r\n' % data
        print(r'Your senddata is %s' % senddata.strip())
        try:
            Client.sendall(senddata.encode())
            respdata = Client.recv(1024)
        except OSError:
            print(r'OSError: Client与Server(%s)Port(%s)的连接未建立' % (host, port))
            respdata = b''
            isTrue = False
            pass
        if not respdata:
            print(r'Server response is Empty !')
            isTrue = False
            pass
        else:
            print(r'Your respdata is %s' % respdata.decode().strip())
            isTrue = False
finally:
    Client.close()
    print(r'与Server(%s)Port(%s)的连接已关闭！' % (host, port))