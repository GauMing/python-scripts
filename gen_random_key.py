#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

__author__ = 'Kohaku'

'''
generate random keys based on given key-length and number of keys
'''
def random_key(num, length):
    ret = set()
    str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    for i in range(num):
        key = ''
        for j in range(length):
            key += random.choice(str)
        if key not in ret:
            ret.add(key)
    return ret

random_key(5, 20)
