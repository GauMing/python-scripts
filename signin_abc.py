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
import logging
from win32com.client import Dispatch

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='signinLogs.log',
                    filemode='a')


class Abc:
    s = requests.Session()

    def signin(self):
        deadline = "08:30:00"
        nowtime = time.ctime()[-13:-5]
        nowday = time.ctime()[0:3]

        if nowday == "Sat" or nowday == "Sun":
            logging.info("Running at %s", nowday)
            return

        if deadline < nowtime:
            logging.info("QUIT. It's late.")
            return

        logging.info("Start running for %s...", self.u.upper())
        ie = Dispatch('InternetExplorer.Application')
        ie.visible = 1

        ie.navigate("http://web.abc/portal/")
        while ie.ReadyState != 4:
            time.sleep(1)
        logging.info("mainpage loaded")

        document = ie.Document
        document.getElementById("UserName").value = self.u
        document.getElementById("Token").value = self.p
        document.getElementById("saveCal").click()

        # wait in case cookies not loaded
        time.sleep(3)

        ie.navigate('http://kfzxsoi.zh.abc/attendance/userinfo.nsf/xpIndex.xsp')
        while ie.ReadyState != 4:
            time.sleep(1)
        logging.info("xpIndex loaded")

        ie.navigate('http://kfzxsoi.zh.abc/attendance/userinfo.nsf/xpSignLogsOfMy.xsp')
        while ie.ReadyState != 4:
            time.sleep(1)
        logging.info("xpSignLogs loaded")

        try:
            document.getElementById("view:_id1:btnSignIN").click()
        except:
            logging.error("btn sign-in not found...")
            self.sms("Sign in FAILED! btn sign-in not found...")
            return

        signinname = document.getElementById('view:_id1:repeat1:0:cfName').innerHtml
        signindate = document.getElementById('view:_id1:repeat1:0:cfDate').innerHtml
        signintime = document.getElementById('view:_id1:repeat1:0:cfTime').innerHtml

        today = datetime.date.today()
        if signindate == str(today):
            if signintime < deadline:
                smscontent = "%s %s Success.%s" % (signinname, signindate, signintime)
            else:
                smscontent = "Failed. It's late."

            logging.info("Signed in SUCCESS.")
            self.sms(smscontent)
            self.killie()
        else:
            logging.info("Oh, you son of a biscuit.")
            logging.error("Failed. Date ERROR. Restart in 10 sec...")
            self.killie()
            time.sleep(10)
            self.signin()

    def sms(self, content):
        headers = {
            'Referer': 'http://itable.abc/iTable/homepage/HomePageAction_loadHomePageSync.action',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        }

        payload = {
            'RegisterName': 'usr',
            'Token': 'pwd',
            'AuthenticationType': '0'
        }
        mainurl = "http://itable.abc/iTable/login/LoginAction_login0.action"
        self.s.post(mainurl, data=payload, headers={'Referer': 'http://web.abc/portal/'})

        smsdata = {
            'msgVO.toMobile': '[{"name":"%s","mobile":"%s","cardId":" "}]' % (self.t, self.t),
            'msgVO.content': content
        }
        rr = self.s.post('http://itable.abc/iTable/msg/insertMessageSend.action', data=smsdata, headers=headers)
        if 'success' in rr.text:
            logging.info("Message sent(%s): %s", self.u, content)

    @staticmethod
    def killie():
        time.sleep(1)
        ret = os.system('tasklist | find "iexplore.exe"')  # if exist iexplore, return 0
        if not ret:
            os.system('taskkill /f /im iexplore.exe')
        logging.info("IE killed.")

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
    Abc(u, p, t)
    time.sleep(10)
