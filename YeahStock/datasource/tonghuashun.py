#! /usr/bin/env python
# -*- coding:utf-8 -*-


import os
import re
import requests

from pyquery import PyQuery as pq

# 从同花顺网站获取股票数据列表
URL = 'http://q.10jqka.com.cn/index/index/board/{board}/field/zdf/order/desc/page/{page}/ajax/1/'
headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Accept - Encoding':'gzip, deflate',
               'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection':'Keep-Alive',
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}


def getStockList(board = 'all', page = 1):
    if board == 'all':
        for b in ['hs', 'ss', 'zxb', 'cyb', 'kcb']:
            getStockList(b)
    else:
        url = re.sub(r'\{board\}', board, URL)
        url = re.sub(r'\{page\}', page, url)
        r = requests.get(url, headers = headers)
        html = pq(r.content.decode('gbk').encode('utf-8', 'ignore').decode('utf-8', 'ignore'))

        trList = html('tbody').find('tr')
        for tr in trList:
            code = pq(tr).find('td').eq(1).text()
            name = pq(tr).find('td').eq(2).text()
            print('code: ' + code + ', name: ' + name)

getStockList('hs', '1')
