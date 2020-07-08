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
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>邮件提醒</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>

<body style="margin: 0; padding: 0;">

<table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse;">
    <tr>
        <td>
            <div style="border: #36649d 1px dashed;margin: 30px;padding: 20px">
                <label style="font-size: 18px;color: #36649d;font-weight: bold">你好，必测接口测试报告，请查收~</label>
                <p style="font-size: 20px"><label style="font-weight: bold">%s</label>环境刚刚发布了后台代码，并进行了自动化测试</p>
                <p style="font-size: 16px">测试环境：<label style="font-weight: bold">%s</label></p>
                <p style="font-size: 16px">发布时间：<label style="font-weight: bold">%s</label></p>
                <p style="font-size: 16px">发布模块：<label style="font-weight: bold">%s</label></P>
                <p style="font-size: 16px">测试报告查看链接如下：</p>
                <p><a href='http://autotest.lrts.me/test_report/%s'>接口测试报告:%s</a></p>
            </div>
        </td>
    </tr>
    <tr>
        <td>
            <div style="margin: 40px">
                <p style="color:red;font-size: 14px ">（这是一封自动发送的邮件，请勿回复。）</p>

            </div>
        </td>
    </tr>
</table>
</body>
</html>

    """ % ('地球', '地球', '2022-02-09 10:01:00', 'apidemp', 'test_reporter20121212121', 'test_reporter20121212121')
    message = MIMEText(versionDsc, 'html', 'utf-8')
    message['From'] = Header("测试邮箱", 'utf-8')
    message['To'] = Header("自动化测试", 'utf-8')
    subject = '此邮件来自自动化测试'  # 邮件来源
    message['Subject'] = Header(subject, 'utf-8')  # 编码方式
    smtpObj = smtplib.SMTP_SSL('smtp.exmail.qq.com')
    smtpObj.connect(get_conf('email', 'mail_host'), 465)  # 465 为 SMTP 端口号
    smtpObj.login(get_conf('email', 'mail_user'), get_conf('email', 'mail_pass'))
    smtpObj.sendmail(get_conf('email', 'mail_user'), receivers, message.as_string())


def send_emails_multi(receivers: list, envId, pubTime, apimodule, report_name, success_Rate):
    if envId == '4':
        host_names = '地球'
    elif envId == '3':
        host_names = '月亮'
    elif envId == '5':
        host_names = '火星'
    versionDsc = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>邮件提醒</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>

<body style="margin: 0; padding: 0;">

<table align="center" border="0" cellpadding="0" cellspacing="0" width="650" style="border-collapse: collapse;">
    <tr>
        <td>
            <div style="border: #36649d 1px dashed;margin: 30px;padding: 20px">
                <label style="font-size: 18px;color: #36649d;font-weight: bold">你好，必测接口测试报告，请查收~</label>
                <p style="font-size: 20px"><label style="font-weight: bold">%s</label>环境发布了后台代码，并进行了自动化测试</p>
                <p style="font-size: 16px">测试环境：<label style="font-weight: bold">%s</label></p>
                <p style="font-size: 16px">发布时间：<label style="font-weight: bold">%s</label></p>
                <p style="font-size: 16px">发布模块：<label style="font-weight: bold">%s</label></P>
                <p style="font-size: 16px">用例通过率：<label style="font-weight: bold">%s</label></P>
                <p style="font-size: 16px">测试报告查看链接如下：</p>
                <p><a href='http://autotest.lrts.me/test_report/%s'>本次测试结果:%s</a></p>
                <p><a href='http://autotest.lrts.me/test_report_list10/'>近10次测试结果</a></p>
            </div>
        </td>
    </tr>
    <tr>
        <td>
            <div style="margin: 40px">
                <p style="color:red;font-size: 14px ">（这是一封自动发送的邮件，请勿回复。）</p>
            </div>
        </td>
    </tr>
</table>
</body>
</html>
    """ % (host_names, host_names, pubTime, apimodule, str(success_Rate) + '%', report_name, report_name)
    message = MIMEText(versionDsc, 'html', 'utf-8')
    message['From'] = Header("测试邮箱", 'utf-8')
    message['To'] = Header("自动化测试", 'utf-8')
    subject = '此邮件来自自动化测试'  # 邮件来源
    message['Subject'] = Header(subject, 'utf-8')  # 编码方式
    smtpObj = smtplib.SMTP_SSL('smtp.exmail.qq.com')
    smtpObj.connect(get_conf('email', 'mail_host'), 465)  # 465 为 SMTP 端口号
    smtpObj.login(get_conf('email', 'mail_user'), get_conf('email', 'mail_pass'))
    smtpObj.sendmail(get_conf('email', 'mail_user'), receivers, message.as_string())
