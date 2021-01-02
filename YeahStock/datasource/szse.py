#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import time

import utils
import ServerAdapter as sa

import Logger

# 从深圳证券交易所获取数据

logger = Logger.getLogger('szse')

URL = 'http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1110&TABKEY=tab1'

def getStockList(mkt = '', page = 1):
    retList = []

    if mkt == '':
        for mkt in ['main', 'sme', 'nm']:
            getStockList(mkt, 1)
    else:
        r = requests.get(URL, params = {'selectModule': mkt, 'PAGENO': page}, headers = utils.REQUEST['headers'])
        data = r.json()[0]
        stockList = data['data']
        pageCount = data['metadata']['pagecount']
        
        for s in stockList:
            m = re.match(r'.+\<u\>\s*(.+)\s*\</u\>', s['agjc'])
            stock = {
                'code': s['agdm'],
                'name': re.sub(r'\s+', '', m.group(1)),
                'market': mkt,
                'exchange': 'szse',
                'listingDate': s['agssrq']
            }
            retList.append(stock)

        sa.addStocks(retList)
        
        logger.info(retList)

        if page < 1 and page * 20 < pageCount:
            time.sleep(5)
            getStockList(mkt, page + 1)

    #return retList             
    

# 获取实时数据
# http://www.szse.cn/api/market/ssjjhq/getTimeData?marketId=1&code=300311
def get_tick_data(code):
    url = config.URL['Szse']['Tick'].format(code = code)
    r = requests.get(url)


#def get_day_line_data(code):


getStockList('sme', 1)

