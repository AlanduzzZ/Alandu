#!/usr/bin/python3.5
#-*- coding:utf-8 -*-

from UserManage import findstr

userdata = {'user_exists': None,  'user_home': None, 'user_env': None, 'user_sudo': None}

class Userinfo(object):

    def __init__(self, username):
        self.__username = username

    def passwdfile(self):
        global userdata
        __filepath = r'/etc/passwd'
        __getUserinfo = findstr(self.__username, __filepath)
        if len(__getUserinfo) > 0:
            __getUserinfo = __getUserinfo.split(':')
            userdata['user_exists'] = 'Yes'
            userdata['user_home']   = __getUserinfo[5]
            userdata['user_env']    = __getUserinfo[6]
            return userdata
        else:
            userdata['user_exists'] = 'No'
            userdata['user_home'] = None
            userdata['user_env'] = None
            return userdata
            pass

    def sudouser(self):
        global userdata
        __filepath = r'/etc/sudoers'
        __getUserinfo = findstr(self.__username, __filepath)
        if len(__getUserinfo) > 0:
            userdata['user_sudo']  = 'Yes'
            return userdata
        else:
            userdata['user_sudo'] = 'No'
            return userdata
            pass

    def getUserinfo(self):
        global userdata
        user = Userinfo(self.__username)
        user.passwdfile()
        user.sudouser()
        return userdata

    def print_user(self):
        print(self.__username)