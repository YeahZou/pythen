#! /usr/bin/env python
# -*- coding:utf-8 -*-


import os
import re
import requests

from pyquery import PyQuery as pq

from yeahstock.utils import UrlUtils as uu

# 从同花顺网站获取股票数据列表
def getStockList(board = 'all', page = 1):
    if board == 'all':
        for b in ['hs', 'ss', 'zxb', 'cyb', 'kcb']:
            getStockList(b)
    else:
        url = uu.get_tonghuashun_stock_list_url(board, page) 
        r = requests.get(url, headers = uu.get_request_head())
        html = pq(r.content.decode('gbk').encode('utf-8', 'ignore').decode('utf-8', 'ignore'))

        trList = html('tbody').find('tr')
        for tr in trList:
            code = pq(tr).find('td').eq(1).text()
            name = pq(tr).find('td').eq(2).text()
            print('code: ' + code + ', name: ' + name)


if __name__ == "__main__" and __package__ is None:
    __package__ = "datasource"
    __name__ = 'datasource'
