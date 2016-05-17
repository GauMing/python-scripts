#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Kohaku'

'''
generate an image mixed with several small images after formatted, hollow out a heart in the center
'''

import PIL.Image as Image
import random
import os


def resizePics(dir, resizeX, resizeY):
    imgs = os.listdir(dir)
    for img in imgs:
        im = Image.open(os.path.join(dir, img))
        width, height = im.size
        cube_size = min(width, height)
        box = (0, 0, cube_size, cube_size)
        region = im.crop(box)
        im = region.resize((resizeX, resizeY), Image.ANTIALIAS)
        im.save(os.path.join(dir, img))


def renameFiles(dir):
    index = 1
    pics = os.listdir(dir)
    for pic in pics:
        name_after = dir + str(index) + '.jpg'
        name_before = os.path.join(dir, pic)
        os.rename(name_before, name_after)
        index += 1


def concatPics(dir, imgCount):
    toImageWidth = 2500
    toImageHeight = 1600
    index = 1
    cube_size = 100
    toImage = Image.new('RGBA', (toImageWidth, toImageHeight))
    blankImage = Image.open(dir + 'blank.jpg')
    theHeart = [(3, 1), (4, 1), (11, 1), (12, 1), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (9, 2), (10, 2), (11, 2),
                (12, 2), (13, 2), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3),
                (11, 3), (12, 3), (13, 3), (14, 3), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4),
                (9, 4), (10, 4), (11, 4), (12, 4), (13, 4), (14, 4), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5),
                (7, 5), (8, 5), (9, 5), (10, 5), (11, 5), (12, 5), (13, 5), (14, 5), (2, 6), (3, 6), (4, 6), (5, 6),
                (6, 6), (7, 6), (8, 6), (9, 6), (10, 6), (11, 6), (12, 6), (13, 6), (3, 7), (4, 7), (5, 7), (6, 7),
                (7, 7), (8, 7), (9, 7), (10, 7), (11, 7), (12, 7), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8),
                (10, 8), (11, 8), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9), (10, 9), (6, 10), (7, 10), (8, 10), (9, 10),
                (7, 11), (8, 11)]
    offsetX = 4
    offsetY = 1
    for y in xrange(16):
        for x in xrange(25):
            if (x - offsetX, y - offsetY) in theHeart:
                toImage.paste(blankImage, (x * cube_size, y * cube_size))
            else:
                pic = dir + str(random.randint(1, imgCount)) + '.jpg'
                fromImage = Image.open(pic)
                toImage.paste(fromImage, (x * cube_size, y * cube_size))
                index += 1
    toImage.save('./result.jpg')


dir = './img/'
# renameFiles(dir)
# resizePics(dir, 100, 100)
concatPics(dir, 100)

# init blank
# resizePics('./blank/', 100, 100)
