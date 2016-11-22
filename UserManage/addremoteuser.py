#!/usr/bin/python3.4
#-*- coding:utf-8 -*-

from Testhost import *
from addlocaluser import *
from ServerAndClient import Client
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-H','--host',help='host ip')
parser.add_argument('-P','--port',help='host port,default is 22',type=int,default=22)
parser.add_argument('-U','--username',help='username')
parser.add_argument('-S','--sudo',help='whether sudo,default is No',default='No')
args = parser.parse_args()

data1 = {'tag': 'getuserinfo', 'username': args.username}

#主机是否可达
Hoststatus = SSHTest_host(args.host, args.port)
if Hoststatus[args.host] == 'DOWN':
    raise SystemExit('Host {} is DOWN'.format(args.host))
else:
    pass

#本地用户是否已经添加
userinfo = Userinfo(args.username).getUserinfo()
if userinfo['user_exists'] == 'Yes':
    pass
else:
    raise SystemExit('Please add localuser {}'.format(args.username))

#远程主机是否已存在该账号
if Client.SocketClient(data1) == 'Yes':
    raise SystemExit('User {} is already exists'.format( args.username))
else:
    pass

with open(r'/data/backup/authorized_keys_bak/{}.pub'.format(args.username), 'r') as f:
    data2 = {'tag': 'addremoteuser', 'username': args.username, 'sudo': args.sudo, 'key': f.read()}

#在远程主机添加账号，以及是否添加sudo权限
addremoteuser = Client.SocketClient(data2)
print(addremoteuser)