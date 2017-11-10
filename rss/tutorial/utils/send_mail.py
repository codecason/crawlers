# --coding: utf-8 -*-

import pymongo
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime
import getpass

def send_email2():
    sender = 'sender@163.com'
    receivers = ['receiver@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(u'Python 邮件发送测试...', 'plain', 'utf-8')
    message['From'] = Header("菜鸟教程", 'utf-8')
    message['To'] =  Header("测试", 'utf-8')
    
    subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(subject, 'utf-8')

    mailhost = 'smtp.163.com'
    try:
        smtp_handler = smtplib.SMTP()
        smtp_handler.connect(mailhost, 25)
        mail_user = raw_input('user')
        mail_pass = getpass.getpass()
        smtp_handler.login(mail_user, mail_pass)
        smtp_handler.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException, e:
        print u"Error: 无法发送邮件"
        print e