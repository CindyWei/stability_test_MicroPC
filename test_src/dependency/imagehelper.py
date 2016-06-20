#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from PIL import Image
import math
import operator
import compare_images


def CompareImage(srcpath, destpath, rate):
    image1 = Image.open(srcpath)
    image2 = Image.open(destpath)
    h1 = image1.histogram()
    h2 = image2.histogram()
    # rms == 0，则完全相同
    rms = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1) )
#     if rms == 0:
#         return True
    if rms < ((1 - rate) *100):
        return True
    else:
        return False

def CropImage(srcpath, destpath, x0, y0, x1, y1):
    img = Image.open(srcpath)
    region = (x0, y0, x1, y1)
    cropImg = img.crop(region)
    cropImg.save(destpath, quality=100)
    
# find region of dest image in src image, if found return the center position of dest image, else None
# assume src.size.x % dest.size.x == 0 && src.size.y % dest.size.y == 0
# rect is the rect want to compare, eg we don't want to compare all the dest image but only some rect of image, then use the rect
# if rect set to None, all the dest image will be compare
def FindImage(srcpath, destpath, rect, rate=50):
    src  = Image.open(srcpath)
    dest = Image.open(destpath)
    src_x, src_y = src.size
    dest_x, dest_y = dest.size
    max_rate = 0
    ret = None
    if src_x % dest_x == 0 and src_y % dest_y == 0:
        item_x = src_x / dest_x
        item_y = src_y / dest_y
        for j in range(item_y):
            for i in range(item_x):
                crop_image_path = os.path.join(os.path.dirname(srcpath), 'applist_crop_%s_%s.jpg' % (i, j))
                CropImage(srcpath, crop_image_path, i * dest_x, j * dest_y, (i + 1) * dest_x, (j + 1) * dest_y)
                similarity = compare_images.FuzzyImageCompare(Image.open(crop_image_path), Image.open(destpath), rect).similarity()
                if similarity > rate:
                    if similarity > max_rate:
                        max_rate = similarity
                        # return center of the picture
                        ret = (i * dest_x + dest_x / 2, j * dest_y + dest_y / 2)
                        print('found image @ (%s, %s, %s)' % (i , j, similarity))
    return ret
