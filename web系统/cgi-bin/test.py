#!D:\phpstudy_pro\Extensions\Apache2.4.39\cgi-bin\venv\Scripts\python.exe
#coding=utf-8
import codecs, sys
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
print ("Content-type:text/html\n\n")
print                               # 空行，告诉服务器结束头部
print ('<html>')
print ('<head>')
print ('<meta charset="utf-8">')
print ('<title>Hello Word！</title>')
print ('</head>')
print ('<body>')
print ('<h2>Hello Word!你好啊</h2>')
print ('</body>')
print ('</html>')