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
    index = 0
    while index < len(hexStr):
        url = ""
        #取8位
        segment = hexStr[index:index + 8]
        #将他看成16进制串与0x3fffffff(30位1)与操作, 即超过30位的忽略处理
        segment = bin(int(segment, 16) & 0x3fffffff)[2:]
        first_len = 6
        if len(segment) % 6 > 0:
            first_len = len(segment) % 6
        start = 0
        for i in range(1, 6):
            if start > len(segment) - 1:
                break
            end = first_len + (i - 1) * 6
            url += codeArray[int('0b' + segment[start:end], 0)]
            start = end
        urls.append(url)
        index += 8
    return urls

if __name__ == '__main__':
    #测试一下
    import os
    i = 500
    while i > 0:
        print shortenURL(os.urandom(random.randint(5, 32)).encode('hex'))[random.randint(0, 3)]
        i -= 1
