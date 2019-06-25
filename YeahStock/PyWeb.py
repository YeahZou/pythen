#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import requests

class PyWeb:
    '使用Python模拟各种web动作方法类'
    def __init__(self):
        print("init class PyWeb")

    def GET(self, url):
        r = requests.get(url)
        return r.text
