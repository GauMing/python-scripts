#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
@Script name:       getzhihu.py
@Author:            Kohaku
@Created at:        2016/3/17 19:17
@Description:       description
"""

import requests
from bs4 import BeautifulSoup

class zhihu(object):
    s = requests.Session()
    url = "https://www.zhihu.com/login/email"

    def get_content(self):
        payload= {
            'email': 'gmkohaku@gmail.com',
            'password': 'x19901012520',
            'remember_me': 'true',
            '_xsfr': ''
        }
        headers = {

        }
        self.s.post(self.url, data=payload, verify=True)

        self.s.get('https://www.zhihu.com', verify=True)

        collections = self.s.get('https://www.zhihu.com/collections')

        # filepath = 'c:/test.txt'
        # with open(filepath, 'w') as f:
        #     f.write(collections.content)

        ll = []
        soup = BeautifulSoup(collections.content, 'html.parser')
        for link in soup.find_all("a"):
            if 'collection/' in link.get('href') and 'followers' not in link.get('href'):
                ll.append(link.get('href'))
                print link

        print ll.__len__()


z = zhihu()
z.get_content()

