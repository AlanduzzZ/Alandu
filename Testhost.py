#!/usr/bin/python2.6
#-*-coding:utf-8-*-

import warnings
warnings.filterwarnings("ignore")
import paramiko

def SSHTest(hostname, port):
    username = 'root'
    pkey = '/root/.ssh/id_rsa'
    paramiko.util.log_to_file('/usr/local/pateo/sshtest.log')
    s = paramiko.SSHClient()
    isTrue = False
    stdout = ''
    stderr = ''
    try:
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            s.connect(hostname=str(hostname), port=int(port), username=str(username), key_filename=str(pkey), timeout=5)
            stdin, stdout, stderr = s.exec_command('echo 1')
            isTrue = True
        except Exception as e:
            stdout = 'Error:%s %s'%(hostname,e)
            stderr = e
            isTrue = False
            pass
        finally:
            if isTrue == True:
                for std in [stdout, stderr]:
                    for line in std.readlines():
                        return line.strip('\n')
            else:
                return stderr
    finally:
        s.close()
def SSHTest_host(ip, port):
    t = SSHTest(ip, port)
    if len(t) == 1 and int(t) == 1:
       return {ip: 'UP'}
    else:
       return {ip: 'DOWN'}