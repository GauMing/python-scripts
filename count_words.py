#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Kohaku'

'''
count words in data.txt, return words and their occurrence;
'''

import re

with open('./data.txt', 'r') as f:
    data = f.read()

word = re.compile(r'([\w\'-]+)')
dic = {}
for word in word.findall(data):
    if word not in dic:
        dic[word] = 1
    else:
        dic[word] += 1

for i in sorted(dic.items(), key=lambda e: e[1], reverse=True):
    print i
