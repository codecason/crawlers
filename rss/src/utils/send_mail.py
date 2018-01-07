# --coding: utf-8 -*-

import pymongo
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime
import getpass

def send_email(infos, mail_user='', mail_pass=''):
    '''封装信息，发送邮件'''
    print "开始发送邮件"
    # 第三方SMTP服务
    mail_host = 'smtp.126.com' # 使用126的SMTP服务
    # 手动输入用户名和密码
    if mail_user == '':
        mail_user = raw_input("input SMTP username (using 126 SMTP service):")
    if mail_pass == '':
        mail_pass = getpass.getpass()

    sender = mail_user
    receivers = ['receiver@163.com']  # 接收邮件，可设置为你自己的邮箱

    # html_content = load_html_by_hand(infos)
    html_content = load_html_by_jinja2(infos)

    message = MIMEText(html_content, 'html', 'utf-8')
    message['From'] = Header("nobking@126.com", 'utf-8')
    message['To'] = Header("Intern Receiver", 'utf-8')

    subject = '{send_date}实习摘要'.format(send_date=datetime.datetime.today().strftime('%Y-%m-%d'))
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtp_handler = smtplib.SMTP()
        smtp_handler.connect(mail_host, 25) #默认端口25
        smtp_handler.login(mail_user, mail_pass)
        smtp_handler.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException as e:
        print "Error: 无法发送邮件"
        print e

def load_html_by_jinja2(infos):
    from jinja2 import Environment, FileSystemLoader
    import datetime
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('email_template.html')
    base_url = 'http://www.newsmth.net'
    return str(template.render(send_date=datetime.datetime.today().
                    strftime('%Y-%m-%d'), infos=infos,
                    total_num=infos.count(), base_url=base_url))

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