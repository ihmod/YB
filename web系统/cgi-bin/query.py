#!D:\phpstudy_pro\Extensions\Apache2.4.39\cgi-bin\venv\Scripts\python.exe

# coding=utf-8

import codecs
import http.cookies
import os
import sys
import cgi
import mysql.connector
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
form = cgi.FieldStorage()
uname = form.getvalue('query')
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
            mycursor.execute("select  uname,types,remaining_days from user where uname='%s'"%(uname))
            ret = myresult = mycursor.fetchone()  # fetchall() 获取所有记录
            if ret==None:
                print('<h1>没有该用户信息</h1>')
            else:
                print('<h1>')
                print('学号:'+myresult[0]+'<br>')
                if myresult[1]==1:
                    print('类型:永久'+'<br>')
                elif myresult[1]==2:
                    print('类型:包周'+'<br>')
                elif myresult[1]==3:
                    print('类型:包月'+'<br>')
                elif myresult[1]==4:
                    print('类型:单次'+'<br>')
                else:
                    print('类型:未订阅'+'<br>')
                print('剩余天数:', myresult[2], '<br>')
                print('</h1>')
        else:
            print(fail)
    except KeyError:
        print(fail)
