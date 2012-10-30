#!/usr/bin/env python
#encoding=utf-8

import unittest
from shorturl import url


class UrlTestCase(unittest.TestCase):

    def testShortenURL(self):
        self.assertEqual(url.shortenURL("www.163.com"), ['mtKj7', 'v1T3x', 'rSWsK', 'pGl2-'])


