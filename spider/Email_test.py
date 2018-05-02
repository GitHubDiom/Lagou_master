# -*- coding: utf-8 -*-
# !/usr/bin/env python
'''
此文件为测试邮箱功能

'''
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from config.config import *

log_temp = log.Logger()#实例化日志对象
log = log_temp.getLoger('log')
def send_email(text):
# 第三方 SMTP 服务
    mail_host="smtp.163.com"  #设置服务器
    mail_user="diom_wu@163.com"    #用户名
    mail_pass="XXXXXXXXX"   #口令 
    sender = 'diom_wu@163.com'
    receivers = ['diom_wu@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    
    message = MIMEText(text, 'plain', 'utf-8')
    #message['From'] = Header("菜鸟教程", 'utf-8')
    #message['To'] =  Header("测试", 'utf-8')
    
    subject = '程序报错邮件提醒'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException:
        traceback.print_exc()
        print ("Error: 无法发送邮件")


request_url = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
try:
    response = requests.get(request_url)
    print(response.json()['content']['positionResult']['totalCount'])

except Exception:
    send_email(traceback.format_exc())
    log.error(traceback.format_exc())
