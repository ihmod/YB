#!D:\phpstudy_pro\Extensions\Apache2.4.39\cgi-bin\venv\Scripts\python.exe
# coding=utf-8

# CGI处理模块
import cgi
import codecs
import sys
import time
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
token = '5d4565b02217e1761d3b981c1f1c6878'  # md5(admin:123)
time_stamp = int(time.time()) + 12 * 60 * 60  # 10位长度时间戳，生成明天的时间戳
GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'  # GMT格式
expires_time = time.strftime(GMT_FORMAT, time.localtime(time_stamp))  # 格式化

# 创建 FieldStorage 的实例化
form = cgi.FieldStorage()
# 获取数据
u_name = form.getvalue('id')
u_pwd = form.getvalue('pwd')
success = f'''Set-Cookie: token={token};expires={expires_time};path="/cgi-bin/"\nContent-type: text/html;charset=UTF-8\n\n
<script>\nalert('登录成功')\n window.location.href = '../YB/';\n </script>\n'''
fail = f'''Set-Cookie: token=null;\nContent-type: text/html;charset=UTF-8\n\n
<script>alert('账号或密码不正确')\n window.setTimeout(\"location.href='javascript:window.history.back()'\",);</script>\n'''

if u_name == 'admin' and u_pwd == '123':
    print(success)
else:
    print(fail)
