#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


def get_files(list_file):
    """
    返回需要修改的文件列表
    :param list_file: 记录需要修改的文件 一行一个
    :return:
    """
    files = []
    with open(list_file, 'r') as f:
        for line in f:
            files.append(line.replace('\n', ''))
    return files


def rename(file_name):
    """
    将文件名后缀改为 .tmp
    :param file_name: 原始文件名
    """
    new_name = os.path.splitext(file_name)[0] + '.tmp'
    # print file_name, new_name
    os.rename(file_name, new_name)


# list_file = r'C:\Users\Kohaku\Desktop\111.txt'
list_file = sys.argv[1]
for filename in get_files(list_file):
    try:
        rename(unicode(filename, 'utf8'))
    except Exception, e:
        # print str(e)
        pass

raw_input("Finished")
