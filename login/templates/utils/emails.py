#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/18 16:23
# @Author  : caozhuo
# @FileName: emails.py
# @Software: PyCharm
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from login.templates.utils.getconf import get_conf


def send_emails(receivers: list):

    versionDsc = """
    <p>你好，Python接口自动化测试报告...</p>
    <p>报告查看链接如下：</p>
    <p><a href='http://autotest.lrts.me/test_report/'>接口测试报告</a></p>
    """
    message = MIMEText(versionDsc, 'html', 'utf-8')
    message['From'] = Header("测试邮箱", 'utf-8')
    message['To'] = Header("自动化测试", 'utf-8')
    subject = '此邮件来自自动化测试'  # 邮件来源
    message['Subject'] = Header(subject, 'utf-8')  # 编码方式
    smtpObj = smtplib.SMTP_SSL('smtp.exmail.qq.com')
    smtpObj.connect(get_conf('email', 'mail_host'), 465)  # 465 为 SMTP 端口号
    smtpObj.login(get_conf('email', 'mail_user'), get_conf('email', 'mail_pass'))
    smtpObj.sendmail(get_conf('email', 'mail_user'), receivers, message.as_string())
