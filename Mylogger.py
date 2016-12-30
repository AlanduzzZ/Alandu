#!/usr/local/python3/bin/python3.5
#-*- coding:utf-8 -*-

import logging

'''
%(levelno)s: 打印日志级别的数值
%(levelname)s: 打印日志级别名称
%(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
%(filename)s: 打印当前执行程序名
%(funcName)s: 打印日志的当前函数
%(lineno)d: 打印日志的当前行号
%(asctime)s: 打印日志的时间
%(thread)d: 打印线程ID
%(threadName)s: 打印线程名称
%(process)d: 打印进程ID
%(message)s: 打印日志信息
'''

#设置日志记录的格式，以及实例化Formatter
log_format = '%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)s - %(name)s - %(message)s'
logformat  = logging.Formatter(log_format)

#设置logger的记录方式，设置Handler，Handler包含输出方式以及输出格式
console = logging.StreamHandler()             #输出到控制台
console.setFormatter(logformat)               #为console设置日志格式，还可以设置其他属性
logfile = logging.FileHandler('alan.log')   #输出到日志文件
logfile.setFormatter(logformat)               #为logfile设置日志格式

#设置日志实例名
UserManagelog = logging.getLogger('UserManage')             #设置日志名，并实例化，其中UserManagelog为实例名，UserManage经常为日志中打印的标记字段，例如模块名称等

#为日志实例添加记录方式以及日志级别
UserManagelog.addHandler(console)             #输出到控制台
UserManagelog.addHandler(logfile)             #输出到日志文件
UserManagelog.setLevel(logging.DEBUG)         #日志级别
UserManagelog.propagate = False              #日志只输出到这一级，不会输出到基础logger的日志文件中

UserManagelog.debug('debug')
UserManagelog.info('info')
UserManagelog.warn('warn')
UserManagelog.critical('critical')