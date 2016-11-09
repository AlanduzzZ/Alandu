#!/usr/bin/python3.5
#-*- coding:utf-8 -*-

import os
from subprocess import getoutput

def findstr(thestr, filepath):
    if not os.path.exists(filepath):
        raise SystemExit(1)
    else:
        with open(filepath, 'r') as f:
            try:
                output = getoutput('grep -w {} {}'.format(thestr, filepath)).strip()
            except Exception as e:
                raise e
            else:
                return output