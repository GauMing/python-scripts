#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header

'''
用crontab定时访问住建委网站，发现网上申购状态更新发邮件通知
'''
def isUpdata():
    headers = {
        'Referer': 'http://zzfws.bjjs.gov.cn/enroll/home.jsp',
        'Content-Type': 'application/json;charset=UTF-8'
    }
    s = requests.session()
    url = 'http://zzfws.bjjs.gov.cn/enroll/home.jsp'
    r = s.get(url)

    url_checkcode = 'http://zzfws.bjjs.gov.cn/enroll/dyn/checkcode.json'
    params = {
        "active_type": "2"
    }
    r = s.post(url_checkcode, data=json.dumps(params), headers=headers)

    url_json = 'http://zzfws.bjjs.gov.cn/enroll/dyn/enroll/viewEnrollHomePager.json'
    params = {
        "currPage": 1,
        "pageJSMethod": "goToPage"
    }

    r = s.post(url=url_json, data=json.dumps(params), headers=headers)
    print r.text
    dic = json.loads(r.text)
    if dic['flag'] == 1 and 'img_dailog_enrollnone.jpg' not in r.text:
        print "Updated!"
        return True
    return False


def send_mail(content):
    sender = ''
    receiver = ''
    subject = '%s Python自动发送' % content
    smtpserver = 'smtp.163.com'
    username = ''
    password = ''

    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = ''
    msg['To'] = ""
    smtp = smtplib.SMTP()
    smtp.connect('smtp.163.com')
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


def run():
    if isUpdata():
        send_mail('状态更新了！')
    else:
        send_mail('没有状态更新！')


if __name__ == '__main__':
    run()
