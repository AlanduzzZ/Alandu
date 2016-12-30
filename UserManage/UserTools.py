#!/usr/local/python3/bin/python3.5
#-*- coding:utf-8 -*-

import warnings
warnings.filterwarnings("ignore")
import paramiko
from UserManage import findstr
import os
from subprocess import getstatusoutput
import Mylogger

## 工具集以及获取用户信息
class UserTools(object):
    def __init__(self):
        global UserInfo
        UserInfo = {'user_exists': None, 'user_home': None, 'user_env': None, 'user_sudo': None}

    ## 在passwd文件里面查找有没有该用户
    def passwdfile(self, username):
        __filePath = r'/etc/passwd'
        __getUserinfo = findstr(username, __filePath)
        if len(__getUserinfo) > 0:
            __getUserinfo = __getUserinfo.strip(':')
            UserInfo['user_exists'] = 'Yes'
            UserInfo['user_home']   = __getUserinfo[5]
            UserInfo['user_env']    = __getUserinfo[6]
            return UserInfo
        else:
            UserInfo['user_exists'] = 'No'
            UserInfo['user_home'] = None
            UserInfo['user_env'] = None
            return UserInfo

    ## 在sudo文件查找有没有sudo权限
    def sudouser(self, username):
        __filepath = r'/etc/sudoers'
        __getUserinfo = findstr(username, __filepath)
        if len(__getUserinfo) > 0:
            UserInfo['user_sudo']  = 'Yes'
            return UserInfo
        else:
            UserInfo['user_sudo'] = 'No'
            return UserInfo

    ## 经过查找，汇总用户信息
    def getUserinfo(self, username):
        user = UserTools()
        user.passwdfile(username)
        user.sudouser(username)
        Mylogger.UserManagelog.info(UserInfo)
        return UserInfo

    def getUserName(self, username):
        return username

    ## 判断文件夹路径是否存在，不存在自动创建
    def dir_exists(self, dirpath):
        if os.path.exists(r'{}'.format(dirpath)):
            Mylogger.UserManagelog.info('{} is exists'.format(dirpath))
            return '{} is exists'.format(dirpath)
        else:
            os.makedirs(r'{}'.format(dirpath))
            Mylogger.UserManagelog.info('mkdir {} successful'.format(dirpath))
            return 'mkdir {} successful'.format(dirpath)

    ## 操作之前去掉文件权限，操作之后加上文件权限
    def chattr_lock(self, lock):
        self.__lock = lock
        if self.__lock == 'lock':
            getstatusoutput(r'chattr +i /etc/passwd /etc/group /etc/shadow /etc/sudoers /etc/profile')
            Mylogger.UserManagelog.debug('lock file success')
        elif self.__lock == 'unlock':
            getstatusoutput(r'chattr -i /etc/passwd /etc/group /etc/shadow /etc/sudoers /etc/profile')
            Mylogger.UserManagelog.debug('unlock file success')
        else:
            Mylogger.UserManagelog.critical('Value Error')
            raise SystemExit(1)

    ## 增加sudo权限
    def sudoAdd(self, username):
        self.__username = username
        self.__usersudo = '{}\t\tALL=(ALL)\tNOPASSWD: ALL'.format(self.__username)
        self.__findsudo = r''
        self.__findsudo = getstatusoutput('grep -w "{}" /etc/sudoers'.format(self.__username))[1].strip()
        if self.__findsudo == self.__usersudo:
            Mylogger.UserManagelog.info('sudo privilege exists')
            return 'sudo privilege exists'
        else:
            getstatusoutput('echo "{}\t\tALL=(ALL)\tNOPASSWD: ALL" >> /etc/sudoers'.format(self.__username))
            Mylogger.UserManagelog.info('sudo privilege has been granted to {}'.format(self.__username))
            return 'sudo privilege has been granted to {}'.format(self.__username)

    ## 测试主机是否可达
    def SSHTest_host(self, hostip, port):
        self.__hostip       = hostip
        self.__port         = port
        self.__username     = 'root'
        self.__pkey         = '/root/.ssh/id_rsa'
        paramiko.util.log_to_file('/usr/local/pateo/sshtest.log')
        s = paramiko.SSHClient()
        Mylogger.UserManagelog.debug('SSHTest host {} port {} start...'.format(self.__hostip, self.__port))
        isTrue = False
        stdout = ''
        stderr = ''
        try:
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                s.connect(hostname=str(self.__hostip), port=int(self.__port), username=str(self.__username), key_filename=str(self.__pkey ), timeout=5)
                stdin, stdout, stderr = s.exec_command('echo 1')
                isTrue = True
            except Exception as e:
                stdout = 'Error:%s %s' % (self.__hostip, e)
                stderr = e
                isTrue = False
                pass
            finally:
                if isTrue == True:
                    for std in [stdout, stderr]:
                        for line in std.readlines():
                            t = line.strip('\n')
                            if len(t) == 1 and int(t) == 1:
                                Mylogger.UserManagelog.debug({ 'hostip': hostip, 'port': port, 'status': 'UP'})
                                return { 'hostip': hostip, 'port': port, 'status': 'UP'}
                            else:
                                Mylogger.UserManagelog.debug({ 'hostip': hostip, 'port': port, 'status': 'DOWN'})
                                return { 'hostip': hostip, 'port': port, 'status': 'DOWN'}
                else:
                    Mylogger.UserManagelog.critical(stderr)
                    return stderr
        finally:
            Mylogger.UserManagelog.debug('SSHTest host {} port {} close...'.format(self.__hostip, self.__port))
            s.close()