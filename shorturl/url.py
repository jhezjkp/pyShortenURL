#!/usr/bin/env python
#encoding=utf-8

'''
短网址服务
'''

import string
import random
import hashlib

codeArray = string.ascii_letters + string.digits + "-_"


def shortenURL(url):
    '''生成短网址'''
    urls = []
    #首先md5一下生成32位摘要
    md5 = hashlib.md5()
    md5.update(url)
    hexStr = md5.hexdigest()
    urls = []
    for i in range(1, 5):
        #8位字符为一组，将其看成16进制数再与0x3fffffff(30位1)相与
        #再转化成二进制，如果不满30位则在左边补0)
        segment = (bin(int(hexStr[8 * (i - 1):8 * i], 16) & 0x3fffffff)[2:]).rjust(30, '0')
        #6位一组，分成5组
        #将各组转成十进制作为索引值从a-zA-Z_-中取对应的值从而获取5位字符长度的短网址
        url = ""
        for j in range(1, 6):
            url += codeArray[int(segment[6 * (j - 1):6 * j], 2)]
        urls.append(url)
    return urls
