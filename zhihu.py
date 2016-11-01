#!/usr/bin/python3.5
#-*- coding:utf-8 -*-

import requests
import re
import time
import damatuWeb

login_url = 'http://www.zhihu.com/'
#生成要提交的Header
agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
header = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    'User-Agent': agent,
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type':'application/x-www-form-urlencoded'
}

#账号密码
emailaddr = r'xxx@gmail.com'
passwd = r'xxxx'


#打开一个session
s = requests.Session()


#获取网页_xsrf参数
def get_xsrf(url, header):
    r = s.get(url, headers=header)
    cookie = r.headers['Set-Cookie']
    cookie_xsrf = re.findall(r'(?<=_xsrf=).+?(?=; )', cookie)
    return cookie_xsrf[0]

#获取验证码
def get_captcha():
    t = str(int(time.time()*1000))
    captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    captcha_r = s.get(captcha_url, headers=header)
    with open('temp\captcha-1.jpg', 'wb') as f:
        f.write(captcha_r.content)
    captcha = (damatuWeb.dmt.decode('temp\captcha-1.jpg', 200))
#    captcha = input("Please input the captcha:\n")
    return captcha

#生成需要提交的数据
post_data = {
    '_xsrf': get_xsrf(login_url, header),
    'password': passwd,
    'captcha': get_captcha(),
    'captcha_type': 'cn',
#    'remember_me': 'true',
    'email': emailaddr
}

print (post_data)

login = s.post('http://www.zhihu.com/login/email', data=post_data, headers=header)
page = s.get('https://www.zhihu.com/settings/profile', headers=header)
s.close()
print (damatuWeb.dmt.getBalance())
print (login)
print (login.status_code)
print (page)
print (page.status_code)