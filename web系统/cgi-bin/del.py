#!D:\phpstudy_pro\Extensions\Apache2.4.39\cgi-bin\venv\Scripts\python.exe
# coding=utf-8

import codecs
import http.cookies
import os
import sys
import cgi
import mysql

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
form = cgi.FieldStorage()
uname = form.getvalue('delete')
print ("Content-type:text/html;charset=UTF-8\n\n")
fail = "<script>alert('操作失败，请返回登录重试！')\n window.location.href = '../YB/login.html';</script>"
if 'HTTP_COOKIE' in os.environ:
    cookie_string = os.environ.get('HTTP_COOKIE')
    c = http.cookies.SimpleCookie()
    c.load(cookie_string)
    try:
        data = c['token'].value
        if data == '5d4565b02217e1761d3b981c1f1c6878':
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="qd"
            )
            mycursor = mydb.cursor()
            mycursor.execute("delete from user where uname='%s'"%(uname))
            mydb.commit()
            print('<h1>')
            print(mycursor.rowcount, " 条记录删除, ID:", uname)
            print('</h1>')
        else:
            print(fail)
    except KeyError:
        print(fail)
