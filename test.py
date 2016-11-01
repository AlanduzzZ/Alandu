#!/usr/local/python3/bin/python3
#-*- coding:utf-8 -*-
import time
import requests

agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
header = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    'User-Agent': agent,
    'X-Requested-With': 'XMLHttpRequest'
}

s = requests.Session()
t = str(int(time.time() * 1000))
captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
captcha_r = s.get(captcha_url, headers=header)
with open('temp\captcha.jpg', 'wb') as f:
    f.write(captcha_r.content)
s.close()
captcha = input("Please input the captcha:\n")
print (captcha)