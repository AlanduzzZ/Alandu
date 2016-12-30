#!/usr/local/python3/bin/python3.5
#-*- coding:utf-8 -*-

import subprocess

abc = subprocess.getstatusoutput('ipconfig')

print(abc[0])
print(abc[1])