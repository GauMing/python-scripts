#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Kohaku'

'''
easy file modifier
'''

import os, fileinput

basepath = r"\path"


def replace_line(filepath):
    for line in fileinput.input(filepath, inplace=1):
        line = line.replace('old', 'new')
        # Do not forget the "," or there will be blank lines
        print line,


for root, dirs, files in os.walk(basepath):
    for fn in files:
        filepath = os.path.join(root, fn)
        if '.txt' in os.path.splitext(filepath)[1]:
            replace_line(filepath)
