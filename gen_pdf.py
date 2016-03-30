#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pdfcrowd
import re
import requests
import os

__author__ = 'Kohaku'

'''
Gain links and transfer these HTML pages to pdf via pdfcrowd API;
Totally 100 tokens for free;
'''


def get_links():
    s = requests.Session()
    url_root = 'https://www.odoo.com/documentation/9.0/'
    resp = s.get(url_root)
    links = re.findall(r'<a href="(.*?)"', resp.content)
    full_links = set()
    for link in links:
        if link[:4] != 'http' and link[:1] != '#':
            full_links.add(url_root + link)
    return full_links


def gen_pdf():
    client = pdfcrowd.Client("user", "key")

    for item in get_links():
        filepath = r'.\\pdfss\\'
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        filename = re.findall(r'.*/(.*?)\.html', item)[0] + '.pdf'
        output_file = open(filepath + filename, 'wb')
        print item
        try:
            client.convertURI(item, output_file)
            output_file.close()
            print filename + '---DONE'
        except pdfcrowd.Error, why:
            print('Failed: {}'.format(why), filename)
            continue


gen_pdf()
