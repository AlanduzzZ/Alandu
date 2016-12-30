#!/usr/local/python3/bin/python3.5
#-*- coding:utf-8 -*-

from UserTools import *
import os
import pexpect
from ServerAndClient import Client

UserToolsApp = UserTools()

class Tools(object):
    def __init__(self):
        pass

## 在跳板机增加本地用户，管理员用秘钥登录，开发用密码登录
class LLocaluseradd(object):
    def __init__(self, username, usertype, password=r''):
        self.__username            = username
        self.__usertype            = usertype
        self.__password            = password
        self.__userauthorizedkeys  = '{}.pub'.format(self.__username)

    ## 如果是admin，则用秘要登录，开发账号使用密码登录
    def userAdd(self):
        Mylogger.UserManagelog.info('Start userAdd...')
        __UserExists = UserToolsApp.getUserinfo(self.__username)['user_exists']
        if __UserExists is not None:
            if __UserExists == 'Yes':
                Mylogger.UserManagelog.debug('User {} is exists !'.format(self.__username))
                raise SystemExit('User {} is exists !'.format(self.__username))
            else:
                addstatus = {
                    'username': self.__username,
                    'usertype': self.__usertype,
                    'addstatus': None,
                    'addsudo': None,
                    'backupkey': None,
                    'userkey': None
                }
                try:
                    UserToolsApp.chattr_lock('unlock')
                    map(UserToolsApp.dir_exists, [r'/data/home', r'/data/backup/authorized_keys_bak'])
                    getstatusoutput(r'useradd -d /data/home/{} {}'.format(self.__username, self.__username))
                    if self.__usertype != 'admin':
                        getstatusoutput(r'echo {} | passwd --stdin {}'.format(self.__password, self.__username))
                    try:
                        ssh = pexpect.spawn('/usr/bin/su {} -c ssh-keygen'.format(self.__username), timeout=5)
                        ssh.expect(r'which to save the key')
                        ssh.sendline('\r')
                        ssh.expect(r'empty for no passphrase')
                        ssh.sendline('\r')
                        ssh.expect(r'Enter same passphrase again:')
                        ssh.sendline('\r')
                        sshlogfile = open('/root/ssh.log', 'wb')
                        ssh.logfile = sshlogfile
                        ssh.expect(pexpect.EOF)
                    except Exception as e:
                        Mylogger.UserManagelog.critical(e)
                        raise SystemExit(e)
                except Exception as e:
                    Mylogger.UserManagelog.critical(e)
                    raise SystemExit(e)
                else:
                    addstatus['addstatus'] = 'success'
                    if self.__usertype != 'admin':
                        with open(r'/data/home/{}/.bash_profile'.format(self.__username), 'a') as f:
                            f.write('\nif [ "$PS1" ];then\n  . /usr/local/pateo/slogin.sh\nfi')
                    try:
                        if os.path.exists(r'/data/backup/authorized_keys_bak/{}'.format(self.__userauthorizedkeys)):  ##  是否已经存在秘钥，如果存在则改名为.bak文件
                            getstatusoutput(r'mv /data/backup/authorized_keys_bak/{} /data/backup/authorized_keys_bak/{}.bak'.format(self.__userauthorizedkeys, self.__userauthorizedkeys))
                            getstatusoutput(r'mv /data/home/{}/.ssh/id_rsa.pub /data/home/{}/.ssh/authorized_keys'.format(self.__username, self.__username))
                            getstatusoutput(r'cp /data/home/{}/.ssh/authorized_keys /data/backup/authorized_keys_bak/{}'.format(self.__username, self.__userauthorizedkeys))
                    except Exception as e:
                        Mylogger.UserManagelog.critical(e)
                        raise SystemExit(e)
                    else:
                        addstatus['backupkey'] = 'success'
                    if self.__usertype == 'admin':
                        try:
                            UserToolsApp.sudoAdd(self.__username)
                        except Exception as e:
                            Mylogger.UserManagelog.critical(e)
                            raise e
                        else:
                            addstatus['addsudo'] = 'Yes'
                            with open('/data/home/{}/.ssh/authorized_keys'.format(self.__username), 'r') as f:
                                addstatus['userkey'] = f.read().strip('\n')
                    else:
                        addstatus['addsudo'] = 'No'
                finally:
                    UserToolsApp.chattr_lock('lock')
                    Mylogger.UserManagelog.debug(addstatus)
                    return addstatus
        else:
            Mylogger.UserManagelog.critical('Get Userinfo Error !')
            raise SystemExit('Get Userinfo Error !')


## 在目的主机增加本地账号 <-- 应部署在目的主机 -->
class RLocaluseradd(object):
    def __init__(self, username, sudo, key):
        self.__username = username
        self.__sudo     = sudo
        self.__key      = key
        self.__userauthorizedkeys = '{}.pub'.format(self.__username)

    def userAdd(self):
        try:
            UserToolsApp.chattr_lock('unlock')
            UserToolsApp.dir_exists('/data/home')
            getstatusoutput('useradd -m -d /data/home/{} -s /bin/bash {}'.format(self.__username, self.__username))
            UserToolsApp.dir_exists('/data/home/{}/.ssh'.format(self.__username))
            getstatusoutput('echo "{}" > /data/home/{}/.ssh/authorized_keys'.format(self.__key.strip('\n'), self.__username))
            getstatusoutput('chown -R {}:{} /data/home/{}'.format(self.__username, self.__username, self.__username))
            getstatusoutput('chmod 700 /data/home/{}/.ssh'.format(self.__username))
            getstatusoutput('chmod 600 /data/home/{}/.ssh/authorized_keys'.format(self.__username))
            if self.__sudo == 'Yes':
                UserToolsApp.sudoAdd(self.__username)
            Mylogger.UserManagelog.info('add user success')
            return ('success')
        except Exception as e:
            Mylogger.UserManagelog.critical(e)
            raise e
        finally:
            UserToolsApp.chattr_lock('lock')

## 在远程主机添加权限
class Remoteuseradd(object):
    def __init__(self, hostip, port, username, sudo):
        self.__hostip    = hostip
        self.__port      = port
        self.__username  = username
        self.__sudo      = sudo

    def userAdd(self):
        ##  检查主机是否存活
        __hoststatus = UserToolsApp.SSHTest_host(self.__hostip, self.__port)
        if __hoststatus['status'] == 'UP':
            Mylogger.UserManagelog.debug(__hoststatus)
        else:
            Mylogger.UserManagelog.critical('Host({}) port({}) is Down !'.format(self.__hostip, self.__port))
            raise SystemExit('Host({}) port({}) is Down !'.format(self.__hostip, self.__port))
        ## 检查跳板机是否存在该用户
        __userexists = UserToolsApp.getUserinfo(self.__username)
        if __userexists['user_exists'] == 'Yes':
            Mylogger.UserManagelog.info(__userexists)
        else:
            Mylogger.UserManagelog.critical('Please add localuser {}'.format(self.__username))
            raise SystemExit('Please add localuser {}'.format(self.__username))
        ## 检查远程主机是否已经存在该账号
        __Testdata = {'tag': 'getUserInfo', 'username': self.__username}
        t = Client.SocketClient(__Testdata)
        if t == 'Yes':
            Mylogger.UserManagelog.critical('User {} is already exists'.format(self.__username))
            raise SystemExit('User {} is already exists'.format(self.__username))
        else:
            with open(r'/data/backup/authorized_keys_bak/{}.pub'.format(self.__username), 'r') as f:
                __adduserdata = {'tag': 'addRemoteUser', 'username': self.__username, 'sudo': self.__sudo, 'key': f.read()}
            __adduser = Client.SocketClient(__adduserdata)
            Mylogger.UserManagelog.info(__adduser)
            return __adduser
