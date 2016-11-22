#!/usr/bin/python3.4
#-*- coding:utf-8 -*-

from addlocaluser import *

def addlocaluser(username, sudo, key):
    chattr_lock('unlock')
    dir_exists('/data/home')
    check_output_shell('useradd -m -d /data/home/{} -s /bin/bash {}'.format(username, username))
    dir_exists('/data/home/{}/.ssh'.format(username))
    with open('/root/test_key', 'w') as f:
        f.write(key)
    check_output_shell('echo "{}" > /data/home/{}/.ssh/authorized_keys'.format(key.strip('\n'), username))
    check_output_shell('chown -R {}:{} /data/home/{}'.format(username, username, username))
    check_output_shell('chmod 700 /data/home/{}/.ssh'.format(username))
    check_output_shell('chmod 600 /data/home/{}/.ssh/authorized_keys'.format(username))
    if sudo == 'Yes':
        addsudo(username)
    chattr_lock('lock')
    return 'Sucessful'