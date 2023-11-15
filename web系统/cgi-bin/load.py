#!D:\phpstudy_pro\Extensions\Apache2.4.39\cgi-bin\venv\Scripts\python.exe
# coding=utf-8
import sys
import codecs
import os
import http.cookies
import time
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
time_stamp = int(time.time()) + 12 * 60 * 60  # 10位长度时间戳，生成明天的时间戳
GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'  # GMT格式
expires_time = time.strftime(GMT_FORMAT, time.localtime(time_stamp))  # 格式化

if 'HTTP_COOKIE' in os.environ:
    cookie_string=os.environ.get('HTTP_COOKIE')
    c=http.cookies.SimpleCookie()
    c.load(cookie_string)
    try:
        data = c['token'].value
        if data=='5d4565b02217e1761d3b981c1f1c6878':
            print(f'''Set-Cookie: token=5d4565b02217e1761d3b981c1f1c6878;expires={expires_time};path='/cgi-bin/'\nContent-type: text/html;charset=UTF-8\n\n''')
            print("状态:已登录 当前用户:admin\n")
        else:
            print("Content-type: text/html;charset=UTF-8\n\n")
            print('fail')
    except KeyError:
        print("Content-type: text/html;charset=UTF-8\n\n")
        print('fail')
else:
    print("Content-type: text/html;charset=UTF-8\n\n")
    print('fail')
