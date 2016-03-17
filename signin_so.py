#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
@ Author:            Kohaku
@ Description:       The script will sign in stackoverflow and log.
"""

import requests
import time

class stackoverflow(object):
	s = requests.Session()

	def signin(self):
		url = 'https://stackoverflow.com/users/login?ssrc=head&returnurl=http%3a%2f%2fstackoverflow.com%2f'
		payload = {
			'fkey': '',
			'ssrc': 'head',
			'email': '@',
			'password': '',
			'oauth-version': '',
			'oauth-server': '',
			'openid-username': '',
			'openid-identifier': ''
		}

		headers = {
			'referer': 'https://stackoverflow.com/users/login?ssrc=head&returnurl=http%3a%2f%2fstackoverflow.com%2f'
		}

		r = self.s.post(url, data=payload, headers=headers)
		if 'logout' in r.content and 'kohaku' in r.content:
			ret = "Success"
		else:
			ret = "Fail"

		filepath = 'soSigninLog.log'
		with open(filepath, 'a') as f:
			f.write(time.ctime() + ' '*10 + ret + '\n')

so = stackoverflow()
so.signin()
