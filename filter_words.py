#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Kohaku'

'''
filter key word in text
'''
word_set = set()
with open('./filtered_words.txt', 'r') as f:
    for x in f.readlines():
        word_set.add(x.strip())

while True:
    text = raw_input('>>')
    if text == 'q':
        break
    for x in word_set:
        if x in text:
            text = text.replace(x, '*' * len(x.decode('utf-8')))
    print text
