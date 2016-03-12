#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
@Script name:       auto_signin.py
@Author:            Kohaku
@Created at:        2016/3/12 13:42
@Description:       The script will sign in on wedkdays and then send messages to respective phones.
"""

import datetime
import os
import requests
import time
from win32com.client import Dispatch


class Abc:
    s = requests.Session()

    def signin(self):
        deadline = "08:30:00"
        nowtime = time.ctime()[-13:-5]
        nowday = time.ctime()[0:3]
        if nowday == "Sat" or nowday == "Sun":
            print "Weekends."
            return

        if deadline < nowtime:
            print "Late."
            return

        ie = Dispatch('InternetExplorer.Application')
        ie.visible = 1

        ie.navigate("http://web.abc/portal/")
        while ie.ReadyState != 4:
            time.sleep(1)
            print "sleep for mainpage..."
        print "mainpage loaded"

        document = ie.Document
        document.getElementById("UserName").value = self.u
        document.getElementById("Token").value = self.p
        document.getElementById("saveCal").click()

        # wait in case cookies not loaded
        time.sleep(1)

        ie.navigate('http://kfzxsoi.zh.abc/attendance/userinfo.nsf/xpIndex.xsp')
        while ie.ReadyState != 4:
            time.sleep(1)
            print "sleep for xpIndex..."
        print "xpIndex loaded"

        ie.navigate('http://kfzxsoi.zh.abc/attendance/userinfo.nsf/xpSignLogsOfMy.xsp')
        while ie.ReadyState != 4:
            time.sleep(1)
            print "sleep for xpSignLogs..."
        print "xpSignLogs loaded"

        try:
            document.getElementById("view:_id1:btnSignIN").click()
        except:
            print "Cannot find the sign in btn, restart in 10 sec..."
            time.sleep(10)
            self.signin()

        signinname = document.getElementById('view:_id1:repeat1:0:cfName').innerHtml
        signindate = document.getElementById('view:_id1:repeat1:0:cfDate').innerHtml
        signintime = document.getElementById('view:_id1:repeat1:0:cfTime').innerHtml

        smscontent = ""
        today = datetime.date.today()
        if signindate == str(today):
            if signintime < deadline:
                smscontent = "%s %s Success. %s" % (signinname, signindate, signintime)

            else:
                smscontent = "Failed. Signed in after deadline."
        else:
            print "Sign in FAILED! Restart in 10 sec"
            self.killie()
            time.sleep(10)
            self.signin()

        print smscontent
        self.sms(smscontent)
        self.killie()

    def sms(self, content):
        url_sms = "http://itable.abc/iTable/msg/toSendSmsPage.action?appBusinessId=duanxin"
        headers = {
            'Referer': 'http://itable.abc/iTable/homepage/HomePageAction_loadHomePageSync.action',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        }

        payload = {
            'RegisterName': 'usr',
            'Token': 'pwd'
        }
        mainUrl = "http://itable.abc/iTable/login/LoginAction_login0.action"
        signin = self.s.post(mainUrl, data=payload, headers={'Referer': 'http://web.abc/portal/'})

        r = self.s.get(url_sms)

        smsdata = {
            'msgVO.toMobile': '[{"name":"%s","mobile":"%s","cardId":" "}]' % (self.t, self.t),
            'msgVO.content': content
        }
        rr = self.s.post('http://itable.abc/iTable/msg/insertMessageSend.action', data=smsdata, headers=headers)
        if 'success' in rr.text:
            print "Msg sent: %s" % content

    def killie(self):

        time.sleep(1)
        ret = os.system('tasklist | find "iexplore.exe"')  # if exist, return 0
        if not ret:
            os.system('taskkill /f /im iexplore.exe')

    def __init__(self, u, p, t):

        self.u = u
        self.p = p
        self.t = t
        self.signin()

person_tuple = [
    'usr&pwd&tel',
]

for person in person_tuple:
    u, p, t = person.split("&")
    print u, p, t
    Abc(u, p, t)
    time.sleep(10)
