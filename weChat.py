#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import time
import os
import xml.dom.minidom


class weChat:
    def __init__(self):
        self.uuid = ''
        self.session = requests.session()
        self.QRImagePath = os.path.join(os.getcwd(), 'qrcode.jpg')
        self.redirect_uri = ''
        self.skey = ''
        self.sid = ''
        self.uin = ''
        self.pass_ticket = ''
        self.base_uri = ''

    def get_uuid(self):
        url = 'https://login.weixin.qq.com/jslogin'
        params = {
            'appid': 'wx782c26e4c19acffb',
            'fun': 'new',
            'lang': 'zh_CN',
            '_': int(time.time()),
        }
        r = self.session.get(url=url, params=params, verify=False)
        data = r.text
        regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"'
        pm = re.search(regx, data)

        if pm:
            code = pm.group(1)
            self.uuid = pm.group(2)
            return code == '200'
        return False

    def show_QRImage(self):
        url = 'https://login.weixin.qq.com/qrcode/' + self.uuid
        r = self.session.get(url=url, verify=False)
        f = open(self.QRImagePath, 'wb')
        f.write(r.content)
        f.close()
        time.sleep(1)
        os.startfile(self.QRImagePath)

    def wait4login(self):
        tip = 0
        url = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?tip=%s&uuid=%s&_=%s' % (
            tip, self.uuid, int(time.time()))
        r = self.session.get(url=url, verify=False)
        data = r.text

        code = re.findall(r'window.code=(.*?);', data)[0]

        if code == '201':
            print "已扫描"
        if code == '200':
            self.redirect_uri = re.findall(r'window.redirect_uri="(\S+?)";', data)[0]
            self.redirect_uri += '&fun=new&version=v2&lang=zh_CN'
            self.base_uri = self.redirect_uri[:self.redirect_uri.rfind('/')]
        return code

    def login(self):
        r = self.session.get(url=self.redirect_uri, verify=False)
        r.encoding = 'utf-8'
        data = r.text
        print data
        tree = xml.dom.minidom.parseString(data)
        root = tree.documentElement
        for node in root.childNodes:
            if node.nodeName == 'skey':
                self.skey = node.childNodes[0].data
            elif node.nodeName == 'wxsid':
                self.sid = node.childNodes[0].data
            elif node.nodeName == 'wxuin':
                self.uin = node.childNodes[0].data
            elif node.nodeName == 'pass_ticket':
                self.pass_ticket = node.childNodes[0].data
        if '' in (self.skey, self.sid, self.uin, self.pass_ticket):
            return False

        return True

    def send_msg(self, msg_content):


    def run(self):
        self.get_uuid()
        self.show_QRImage()

        while self.wait4login() != '200':
            pass
        os.remove(self.QRImagePath)

        if self.login():
            print 'Login succeed.'
        else:
            print 'login failed.'


a = weChat()
a.run()

