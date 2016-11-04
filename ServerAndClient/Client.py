#!/usr/local/python3/bin/python3
#-*- coding:utf-8 -*-

from socket import *

host = '127.0.0.1'
port = 20001
addr = (host, port)
Client = socket(AF_INET, SOCK_STREAM)
Client.connect(addr)
while True:
    data = input('Please input the data :')
    if not data or data==r'exit' or data==r'EXIT':
        break
    senddata = '%s\n' % data
    print(r'Your senddata is %s' % senddata)
    Client.sendall(senddata.encode())
    respdata = Client.recv(1024)
    if not respdata:
        print(r'Server response is Empty !')
        break
    else:
        print(r'Your respdata is %s' % respdata.decode())
Client.close()