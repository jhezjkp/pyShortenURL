#!/usr/bin/env python
#encoding=utf-8

import os
import random
import unittest
from shorturl import url


class UrlTestCase(unittest.TestCase):

    def testShortenURL(self):
        self.assertEqual(url.shortenURL("www.163.com"), ['mtKj7', 'v1T3x', 'rSWsK', 'pGl2-'])

    def testShortenURLRandom(self):
        for i in range(1, 100):
            self.assertEqual(len(url.shortenURL(os.urandom(random.randint(5, 32)).encode('hex'))), 4)


