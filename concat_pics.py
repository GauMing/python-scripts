#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Kohaku'

'''

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
    index = 100
    pics = os.listdir(dir)
    for pic in pics:
        name_after = dir + str(index) + '.jpg'
        name_before = os.path.join(dir, pic)
        os.rename(name_before, name_after)
        index += 1


def concatPics(dir):
    toImageWidth = 2000
    toImageHeight = 1000
    index = 100
    cube_size = 100
    toImage = Image.new('RGBA', (toImageWidth, toImageHeight))
    for y in xrange(10):
        for x in xrange(20):
            pic = dir + str(random.randint(100, 199)) + '.jpg'
            fromImage = Image.open(pic)
            toImage.paste(fromImage, (x * cube_size, y * cube_size))
            index += 1
    theHeart = [(8,2), (9,2), (11,2), (12,2), (7,3), (8,3), (9,3), (10,3), (11,3), (12,3), (13,3), (7,4), (8,4),
                (9,4), (10,4), (11,4), (12,4), (13,4), (8,5), (9,5), (10,5), (11,5), (12,5), (9,6), (10,6), (11,6),
                (10,6), (10, 7)]
    for point in theHeart:
        blankImage = Image.open(dir + 'blank.jpg')
        toImage.paste(blankImage, (point[0] * cube_size, point[1] * cube_size))
    toImage.save('./1.jpg')


dir = './img/'
renameFiles(dir)
resizePics(dir, 100, 100)
concatPics(dir)

# init blank
# resizePics('./blank/', 100, 100)
