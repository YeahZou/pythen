#!/usr/bin/env python
#

"""
通知模块，当程序出现异常时，通知管理员处理
"""
import smtplib

from_addr = "serveradmin@localhost.com"
to_addrs = ["2544610309@qq.com"]
def sendmail(title, content):
    msg = '''\
        From: {from_addr}
        Subject: {title}
        {content}
    '''.format(from_addr = from_addr, title = title, content = content)
    s = smtplib.SMTP("localhost")
    print(msg)
    ret = s.sendmail(from_addr, to_addrs, msg)
    print(ret)
    s.quit()

sendmail('test', 'this is a test mail')
