#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
确定文件夹中所有.net项目的引用关系

'''

import os
import xml.etree.ElementTree as ET


def get_csproj_files(target_dir):
    '''
    找到所有的.csproj 文件
    :return:
    '''
    csproj_files = []
    dir_lists = os.walk(target_dir)
    for path, dir_list, file_list in dir_lists:
        for file_name in file_list:
            if os.path.splitext(file_name)[1] == '.csproj':
                print(os.path.join(path, file_name))
                csproj_files.append(os.path.join(path, file_name))
    return csproj_files


def get_references(csproj_file):
    '''
    获取一个project的引用
    :param csproj_file:
    :return:
    '''
    root = ET.parse(csproj_file).getroot()
    for person in root.findall('{http://schemas.microsoft.com/developer/msbuild/2003}ItemGroup'):
        # .csproj文件定义了命名空间xmlns，查找的时候加上命名空间
        for ref in person.findall('{http://schemas.microsoft.com/developer/msbuild/2003}ProjectReference'):
            print csproj_file + '-->' + ref.get("Include")

