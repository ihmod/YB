import hashlib
import json
import logging
import smtplib
import time
from email.utils import formataddr
from email.mime.text import MIMEText
from logging import handlers  # 日志分割，一天一分，十天一删

import colorlog as colorlog
import pymysql
import requests
from lxml import etree

# formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
millis = int(round(time.time() * 1000))
colors_config = {
    # 终端输出日志颜色配置
    'DEBUG': 'white',
    'INFO': 'cyan',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

default_formats = {
    # 终端输出格式
    'color_format': '%(log_color)s%(asctime)s-%(name)s-%(filename)s-[line:%(lineno)d]-%(levelname)s-[日志信息]: %(message)s',
    # 日志输出格式
    'log_format': '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
}
formatter1 = colorlog.ColoredFormatter(default_formats["color_format"], log_colors=colors_config)

formatter2 = logging.Formatter(default_formats["log_format"])

yellow = '\033[01;33m'
white = '\033[01;37m'
green = '\033[01;32m'
blue = '\033[01;34m'
red = '\033[1;31m'
end = '\033[0m'
banner = f'''
{yellow}
易班自动打卡项目 #V0.0.1
-------------------------------------------------------------------------
{green}
⣐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣶⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣅⡠⠃⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢹⣿⣇⡀⠀⠀⠀⢀⣤⣤⣤⣾⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀
⢸⣿⣿⣷⡀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣶
⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣤⡀⠀⠀⠀⣀⣀⣤⣾
⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇
⠀⠀⠉⠙⠉⠉⠁⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⠟⠋⠁⠀⠀

'''

def logdefine():
    logger = logging.getLogger()  # 创建记录器
    logger.setLevel(level=logging.DEBUG)  # 设置记录级别

    # 输出到控制台
    stream_handler = logging.StreamHandler()  # 输出流位置
    stream_handler.setLevel(logging.INFO)  # 输出级别
    stream_handler.setFormatter(formatter1)  # 输出格式

    # 保存日志文件，并自动分割器，按文件大小分割
    rotating_file_handler = handlers.RotatingFileHandler(filename='D:\phpstudy_pro\WWW\YB\YB.log', mode='a', maxBytes=10 * 1024 * 1024,
                                                         backupCount=2, encoding='utf-8')
    rotating_file_handler.setLevel(logging.INFO)
    rotating_file_handler.setFormatter(formatter2)

    logger.addHandler(rotating_file_handler)  # 添加分割器的日志输出
    logger.addHandler(stream_handler)  # 设置输出流到控制台

    return logger


def wap(list):
    lurl = list[2]
    cookie = list[1]
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Cookie": 'JSESSIONID=' + cookie,
        "Host": "ssgl.hnie.edu.cn",
        "Referer": "http://ssgl.hnie.edu.cn/index",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Android"
    }

    wap = requests.get(lurl, headers=headers)

    rcode = wap.status_code
    selector = etree.HTML(wap.text)

    g = selector.xpath('//div[@id="tabbar-menu"]/ul/li[1]/a/@href')
    list2 = [rcode, ]
    if len(g) == 0:
        rurl = ''
    else:
        rurl = 'http://ssgl.hnie.edu.cn/' + g[0].lstrip("javascript:openWindow('").rstrip("')")
    list2.append(rurl)
    return list2


def md5(pwd):
    pd_md5 = hashlib.md5()
    pd_md5.update(pwd.encode("utf-8"))
    p = list((pd_md5.hexdigest()).lower())
    p.pop(30)
    p.pop(30)
    p.insert(5, 'a')
    p.insert(10, 'b')
    pd = ''.join(p)
    return pd


def stampinfo(list1, list2):
    referer = list2[1]
    url = 'http://ssgl.hnie.edu.cn/content/tabledata/gygl/sign/stu/sign?bSortable_0=false&bSortable_1=true&iSortingCols=1&iDisplayStart=0&iDisplayLength=12&iSortCol_0=3&sSortDir_0=desc&_t_s_=' + str(
        millis)
    cookie = list1[1]
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Cookie": "JSESSIONID=" + cookie,
        "Host": "ssgl.hnie.edu.cn",
        "Referer": referer,
        "User-Agent": "Android",
        "X-Requested-With": "XMLHttpRequest"
    }

    stamp = requests.get(url, headers=headers).text
    sjdm = json.loads(stamp)['aaData'][0]['SJDM']
    dm = json.loads(stamp)['aaData'][0]['DM']
    result = [sjdm, dm]
    return result


def post(user, list1, list2, list3):
    url = 'http://ssgl.hnie.edu.cn/content/gygl/sign/stu/sign?_t_s_=' + str(millis)
    cookie = list1[1]
    referer = list2[1]
    dm = list3[1]
    sjdm = list3[0]
    zb = user[3]
    wz = user[2]
    # print(cookie,referer,dm,sjdm,zb,wz)
    headers = {
        'Host': 'ssgl.hnie.edu.cn',
        'Connection': 'keep-alive',
        'Content-Length': '366',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 12; zh-cn; M2012K10C Build/SP1A.210812.016) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/100.0.4896.127 Mobile Safari/537.36 XiaoMi/MiuiBrowser/17.0.21 swan-mibrowser',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://ssgl.hnie.edu.cn',
        'Referer': referer,
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'JSESSIONID=' + cookie
    }
    data = {'pathFile': '',
            'dm': dm,
            'sjdm': sjdm,
            'zb': zb,
            'wz': wz,
            'ly': 'lbs',
            'qdwzZt': '1',
            'fwwDistance=': '',
            'operationType': 'Update'
            }
    s = requests.post(url, headers=headers, data=data)
    ret=json.loads(s.text)
    result = [s.status_code,ret["result"]]
    return result

def mail(user, mailmsg):
    my_sender = '2306507479@qq.com'  # 发件人邮箱账号
    my_pass = 'subtypozcgvadifi'  # 发件人邮箱密码
    my_user = '519200882@qq.com'  # 收件人邮箱账号

    ret = True
    try:
        text = f'''学号:{user[0]}打卡失败,{mailmsg}'''
        msg = MIMEText(text, 'plain', 'utf-8')
        msg['From'] = formataddr(["易班自动打卡", my_sender], 'utf-8')  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["kk", my_user], 'utf-8')  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "易班打卡失败提醒"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False

    if ret:
        msg = '邮件发送成功'
    else:
        msg = '邮件发送失败'
    return msg


def verify(list):
    ret = True

    if len(list[1]) == 0:
        msg = '-->>获取数据失败'
        ret = False
    else:
        msg = '-->>获取数据成功'
    result = [ret, msg]
    return result


def login(list):
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5",
        "Connection": "keep-alive",
        "Content-Length": "57",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "ssgl.hnie.edu.cn",
        "Origin": "http://ssgl.hnie.edu.cn",
        "Referer": "http://ssgl.hnie.edu.cn/index",
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 12; zh-cn; M2012K10C Build/SP1A.210812.016) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/100.0.4896.127 Mobile Safari/537.36 XiaoMi/MiuiBrowser/17.0.21 swan-mibrowser",
        "X-Requested-With": "XMLHttpRequest"
    }
    url = 'http://ssgl.hnie.edu.cn/website/login'
    pd = md5(list[1])
    data = {
        'uname': list[0],
        'pd_mm': pd
    }
    response = requests.post(url, headers=headers, data=data)
    # 查看响应状态码
    lcode = response.status_code
    # 查看头部Set-Cookie
    cookie = response.headers['Set-Cookie'].split('=', 1)[-1].split(';', 1)[0]

    # 查看响应内容，response.text 返回的是Unicode格式的数据
    lurl = 'http://ssgl.hnie.edu.cn/' + response.text.lstrip('{"goto2":"').rstrip('","url":null}')

    result = [lcode, cookie, lurl]
    return result


def main():
    logger = logdefine()
    logger.info(banner)
    logger.info('项目启动成功')
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', database='qd', charset='utf8')
    cursor = db.cursor()
    cursor.execute('select * from user')
    result = cursor.fetchall()
    for user in result:
    # user=result[4]
        logger.info(
            f'''读取用户数据-->>学号: {user[0]} 类型: {user[4]} 剩余天数:{user[5]}''')  # 类型：1（单次）、2（包周）、3（包月）、4（仅周末连续四周）
        if user[4]!=-1 and user[5]!=0:
            try:
                list1 = login(user)  # 请求发送异常，直接抛出
                result1 = verify(list1)  # 检验数据是否为空以及是否为异常数据,返回[是否成功,消息]
                if result1[0]:
                    logger.info('登录校验' + result1[1])
                    # logger.info(list1)
                else:
                    logger.error('登录校验' + result1[1])
                    # logger.info(list1)
                    msg=mail(user, '账号密码错误或者登录接口变更')
                    logger.info(msg)
                    continue
            except Exception as e:
                text1 = '登录请求异常-->>' + str(e)
                logger.error(text1)
                msg=mail(user, text1)
                logger.info(msg)
                continue

            try:
                list2 = wap(list1)
                result2 = verify(list2)
                if result2[0]:
                    logger.info('获取链接-->>' + result2[1])
                    # logger.info(list2)
                else:
                    logger.error('获取链接-->>' + result2[1])
                    # logger.info(list2)
                    msg=mail(user, '可能是cookie失效或者Xpath更改')
                    logger.info(msg)
                    continue
            except Exception as e:
                text2 = '获取链接异常-->>' + str(e)
                logger.error(text2)
                msg=mail(user, text2)
                logger.info(msg)
                continue

            try:
                list3 = stampinfo(list1, list2)
                result3 = verify(list3)
                if result1[0]:
                    logger.info('获取参数' + result3[1])
                else:
                    logger.error('获取参数' + result3[1])
                    msg=mail(user, '可能是cookie失效或者请求载荷更改')
                    logger.info(msg)
                    continue
            except Exception as e:
                text3 = '获取参数异常-->>' + str(e)
                logger.error(text3)
                msg=mail(user, text3)
                logger.info(msg)
                continue

            try:
                list4 = post(user, list1, list2, list3)
                if list4[1]:
                    logger.info('签到成功-->>' )
                    day = user[5] - 1
                    xh = user[0]
                    sql = "UPDATE user SET remaining_days='%d' where uname='%s'"%(day,xh)
                    # logger.info(sql)
                    ret = cursor.execute(sql)
                    db.commit()
                    if ret == 1:
                        logger.info('数据更新成功 剩余天数:'+str(user[5]))
                    else:
                        logger.error('数据修改失败')
                        msg = mail(user, '数据修改失败')
                        logger.info(msg)
                else:
                    logger.error('签到失败')
                    msg=mail(user,'返回信息异常,请核实该用户是否签到成功')
                    logger.info(msg)
                    continue
            except Exception as e:
                text4 = '提交签到异常-->>' + str(e)
                logger.error(text4)
                msg=mail(user, text4)
                logger.info(msg)
                continue


if __name__ == '__main__':
    main()
