#!/usr/bin/python3.4
#-*- coding:utf-8 -*-

from subprocess import check_output
import os
import functools
import pexpect
from iflocaluser import Userinfo
import sys

check_output_shell = functools.partial(check_output, shell=True, stdin=None, stderr=None)


def dir_exists(dirpath):
    if os.path.exists(r'%s' % dirpath):
        return 'dir is exists'
    else:
        os.makedirs(r'%s' % dirpath)
        return 'mkdir successful'

def adduser(username, password=r''):
    try:
        mkdir = list(map(dir_exists, [r'/data/home', r'/data/backup/authorized_keys_bak']))
        check_output_shell(r'useradd -d /data/home/%s %s' % (username, username))
        if sys.argv[1] != 'admin':
            check_output_shell(r'echo %s | passwd --stdin %s' % (password, username))
        try:
            ssh = pexpect.spawn('/usr/bin/su %s -c ssh-keygen' % username, timeout=5)
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
            raise SystemExit(e)
    except Exception as e:
        raise SystemExit(e)
    else:
        print('adduser successful !')
        if sys.argv[1] != 'admin':
            with open(r'/data/home/{}/.bash_profile'.format(username), 'a') as f:
                f.write('\nif [ "$PS1" ];then\n  . /usr/local/pateo/slogin.sh\nfi')
        try:
            if os.path.exists(r'/data/backup/authorized_keys_bak/{}'.format(userauthorizedkeys)):
                check_output_shell(r'mv /data/backup/authorized_keys_bak/{} /data/backup/authorized_keys_bak/{}.bak'.format(userauthorizedkeys, userauthorizedkeys))
            check_output_shell(r'mv /data/home/{}/.ssh/id_rsa.pub /data/home/{}/.ssh/authorized_keys'.format(username, username))
            check_output_shell(r'cp /data/home/{}/.ssh/authorized_keys /data/backup/authorized_keys_bak/{}'.format(username, userauthorizedkeys))
        except Exception as e:
            raise SystemExit(e)
        else:
            print('backupkey successful !')

def addsudo(username):
    usersudo = '{}\t\tALL=(ALL)\tNOPASSWD: ALL'.format(username)
    fromfile = r''
    try:
        fromfile = check_output_shell('grep -w "{}" /etc/sudoers'.format(username)).decode().strip()
    except Exception as e:
        pass
    if fromfile == usersudo:
        pass
    else:
        try:
            check_output_shell('echo "{}\t\tALL=(ALL)\tNOPASSWD: ALL" >> /etc/sudoers'.format(username))
            return 'add sudo sucessful'
        except Exception as e:
            raise SystemExit(e)

def chattr_lock(lock):
    if lock == 'lock':
        try:
            check_output_shell(r'chattr +i /etc/passwd /etc/group /etc/shadow /etc/sudoers /etc/profile')
        except Exception as e:
            raise SystemExit(e)
    elif lock == 'unlock':
        try:
            check_output_shell(r'chattr -i /etc/passwd /etc/group /etc/shadow /etc/sudoers /etc/profile')
        except Exception as e:
            raise SystemExit(e)
    else:
        raise SystemExit(1)

if __name__ == '__main__':
    if 3 <= len(sys.argv) <= 4:
        if sys.argv[1] == 'admin' and len(sys.argv) == 3:
            pass
        else:
            if sys.argv[1] == 'devel' and len(sys.argv) == 4:
                pass
            else:
                raise SystemExit('Usage: {} [admin|devel] username (passwd) passwd为添加devel账号必选参数'.format(sys.argv[0]))
    else:
        raise SystemExit('Usage: {} [admin|devel] username (passwd) passwd为添加devel账号必选参数'.format(sys.argv[0]))
    userauthorizedkeys = r'{}.pub'.format(sys.argv[2])
    userinfo = Userinfo(sys.argv[2])
    ifuser = userinfo.getUserinfo()['user_exists']
    if ifuser is not None:
        if ifuser == r'Yes':
            raise SystemExit('User {} is exists !'.format(sys.argv[2]))
        elif ifuser == r'No':
            pass
    else:
        raise SystemExit('Get Userinfo Error !')
    if sys.argv[1] == 'admin':
        try:
            chattr_lock('unlock')
            adduser(sys.argv[2])
            addsudo(sys.argv[2])
        except Exception as e:
            raise SystemExit(e)
        finally:
            chattr_lock('lock')
    elif sys.argv[1] == 'devel':
        try:
            chattr_lock('unlock')
            adduser(sys.argv[2], sys.argv[3])
        except Exception as e:
            raise SystemExit(e)
        finally:
            chattr_lock('lock')
    else:
        raise SystemExit('The parameter you entered is incorrect !')