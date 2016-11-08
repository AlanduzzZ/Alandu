#!/usr/bin/python3.4
#-*- coding:utf-8 -*-

import os
import sys
import atexit
import signal
import time
from ServerAndClient.Server import MyServer
from ServerAndClient.Server import MyThreadingTCPServer

def daemonize(pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    #检查当前进程是否已经存在，保证唯一性
    if os.path.exists(pidfile):
        raise RuntimeError(r'Monitor is already running !')
    # 判断文件路径是否存在，如果不存在则创建这些目录
    def dir_exists(dirpath):
        if os.path.exists(r'%s' % dirpath):
            return 'dir is exists'
        else:
            os.makedirs(r'%s' % dirpath)
            return 'mkdir successful'
    map(dir_exists, [pidfile, stdout, stdin])
    #第一次结束当前父进程，创建第一个子进程
    #fork()函数：如果父进程调用，则返回子进程PID，PID肯定大于0；如果子进程调用，那么返回0
    try:
        if os.fork() > 0:               #判断当前是否为子进程，身份是父进程
            raise SystemExit()          #如果是子进程，那么结束父进程，这时候子进程已经开始运行了
    except OSError as e:                #判断创建子进程的时候是否出错，如果出现OSErroe错误，那么抛出异常
        raise RuntimeError(r'Fork #1 failed !')
    #重新为子进程设置会话环境，如果不这么做，会导致一些麻烦
    os.chdir('/')               #重新设置子进程根目录，也就是运行目录。如果不设置，那么子进程将锁定在当前目录下，如果你要对这个目录进行重新挂载等操作，会提示该设备正在忙碌
    os.umask(0)                 #设置子进程对于运行目录的权限，0表示读写可执行权限
    os.setsid()                 #重新开启一个新的进程会话，并设置子进程为该进程会话的首领
    #程序运行到这里，将会杀死父进程，启动子进程，并开启新进程组，将子进程设置为新进程组的进程首领，让子进程失去终端的控制权，不会接受终端的控制信号了
    #第二次结束当前父进程，创建第二个子进程（应该是子进程的子进程）
    try:
        if os.fork() > 0:               #判断当前是否为子进程，身份是父进程（第一次创建的子进程）
            raise SystemExit()          #如果是子进程，结束父进程，第二个子进程开始运行
    except OSError as e:
        raise RuntimeError(r'Fork #2 failed !')
    #将所有的标准输出和错误输出都立刻输出到目的地
    sys.stdout.flush()
    sys.stderr.flush()
    #重定向stdin，stdout，stderr文件到新的文件描述符，因为杀死子进程之后被占用的文件描述符也许并不会释放，所以这里是做一个重定向释放出来
    #os.dup2()函数是将重定向文件描述符，将前一个文件描述符复制到后面一个文件描述符，这样在调用三个标准输入输出的时候将会重定向到指定的文件
    with open(stdin, 'rb', 0) as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open(stdout, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
    with open(stderr, 'ab', 0)as f:
        os.dup2(f.fileno(), sys.stderr.fileno())
    #当前进程为第二个子进程，也是最终需要作为守护进程的进程，需要将PID写入文件，以便调用
    with open(pidfile, 'w') as f:
        print(os.getpid(), file=f)
    def stopit():
        os.remove(pidfile)              #清理PID文件
        sys.stdout.write('Daemon stoped with pid {},{}\n'.format(os.getpid(), time.ctime()))        #记录stop时间到日志
        sys.stdout.flush()              #刷新日志文件
    #注册一个回调函数，当程序非正常退出或者os.exit()退出，则不会执行回调函数，并且回调函数的注册顺序（A,B,C）和执行顺序（C,B,A）是相反的
    atexit.register(lambda: stopit())             #调用stop时的清理操作
    #定义一个进程收到终止信号的时候的操作
    def sigterm_handler(signo, frame):
        raise SystemExit(1)
    #自定义进程信号接收器
    signal.signal(signal.SIGTERM, sigterm_handler)
#到这里，守护进程如何启动已经定义完毕，接下来定义主函数

#主函数先写一个示例，每10秒写一句话到stdout中
def main(host, port):
    sys.stdout.write('Daemon started with pid {},{}\n'.format(os.getpid(), time.ctime()))
    addr = (host, port)
    server = MyThreadingTCPServer(addr, MyServer)
    server.serve_forever()
    sys.stdout.flush()
#现在主函数写完了，接下来写这个守护进程的调用方法

if __name__ == '__main__':
    # 配置主函数需要的参数
    host = '0.0.0.0'
    port = 20001
    #定义PID文件位置，也可以由外
    PIDFILE = r'/tmp/daemon.pid'
    STDOUT = r'/tmp/daemon.log'
    STDERR = r'/tmp/daemon.log'
    #定义接收参数的判断，sys.argv()函数是获取程序执行时的参数，第一个参数是程序本身的名字
    if len(sys.argv) != 2:              #如果参数个数不等于2，也就是程序执行时程序只能有一个参数
        print('Usage: {} [start|stop]'.format(sys.argv[0]), file=sys.stderr)
        raise SystemExit(1)
    if sys.argv[1] == r'start':        #如果参数为start，就开始执行守护进程和主函数
        try:
            daemonize(pidfile=PIDFILE, stdout=STDOUT, stderr=STDERR)        #执行守护进程
        except RuntimeError as e:
            print(e, file=sys.stderr)
            raise SystemExit(1)
        main(host, port)                          #执行主函数
    elif sys.argv[1] == r'stop':      #如果参数为stop，则向守护进程发送终止信号
        if os.path.exists(PIDFILE):
            with open(PIDFILE) as f:
                os.kill(int(f.read()), signal.SIGTERM)
        else:
            print('Not running !', file=sys.stderr)
            raise SystemExit(1)
    else:
        print('Unknown command {!r}'.format(sys.argv[1]), file=sys.stderr)          #这里的{!r}最后出来的结果会把sys.argv[1]用单引号包起来，{!s}不会包起来
        raise SystemExit(1)