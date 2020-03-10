#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import logging
import time
import re
import sys
import json
import demjson
import math

FUND_LIST_URL = 'http://vip.stock.finance.sina.com.cn/fund_center/data/jsonp.php/((/NetValue_Service.getNetValueOpen?page=1&num=40&sort=nav_date&asc=0&ccode=&type2=2&type3='

FUND_HISTORY_NAV_URL = 'https://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?callback=(('

# 字段映射关系
keyMaps = {
    'per_nav': 'perNav',
    'total_nav': 'totalNav',
    'yesterday_nav': 'yesterdayNav',
    'nav_rate': 'navRate',
    'nav_a': 'navA',
    'sg_states': 'status',
    'nav_date': 'date',
    'fund_manager': 'fundManager',
    'jjlx': 'type'
}

def getFundList():
    r = requests.get(FUND_LIST_URL)
    data = r.content.decode('gb2312').encode('utf-8', "ignore").decode('utf-8', 'ignore')
    data = re.sub('^[\s\S]+?\\{', '{', data)
    data = re.sub('\\}\\)[\s\S]+?$', '}', data)
    
    # 将 javascript 格式的 json 转为标准 json
    jsonData = demjson.decode(data, decode_object=convertKey)
    print(jsonData)

# 数据清洗，转换对象的 key 名称
def convertKey(obj):
    for k in keyMaps.keys():
        if k in obj.keys():
            obj[keyMaps[k]] = obj[k]
            del obj[k]
    return obj

#getFundList()


# 基金净值数据格式转换
def convertNav(obj):
    if 'fbrq' in obj:
        obj['date'] = obj['fbrq'][:10]
        obj['perNav'] = float(obj['jjjz'])
        obj['totalNav'] = float(obj['ljjz'])

        del obj['fbrq']
        del obj['jjjz']
        del obj['ljjz']
    return obj


# 根据基金代码获取历史净值数据
# 每次返回 20 条数据，按日期降序排列
def getOnePageFundNav(symbol, page):
    r = requests.get(FUND_HISTORY_NAV_URL, params={'symbol': symbol, 'page': page})
    data = re.sub('^[\s\S]+?\\{', '{', r.text)
    data = re.sub('\\}\\)[\s\S]+?$', '}', data)

    dictData = demjson.decode(data, decode_object=convertNav)
    totalNum = dictData['result']['data']['total_num']
    navList = dictData['result']['data']['data']

    return {'totalNum': int(totalNum), 'navList': navList}

def getFundNavBatch(symbol):
    navList = []
    dictNav = getOnePageFundNav(symbol, 1)
    navList.extend(dictNav['navList'])

    pageNum = math.ceil(dictNav['totalNum'] / 20)

    if pageNum > 1:
        for page in range(2, pageNum + 1):
            dictNav = getOnePageFundNav(symbol, page)
            navList.extend(dictNav['navList'])
    
        for i in range(len(navList) - 1):
            obj = navList[i]
            yesterday = navList[ i + 1 ]
            obj['yesterdayNav'] = yesterday['perNav']
            obj['navA'] = obj['perNav'] - obj['yesterdayNav']
            obj['navRate'] = obj['navA'] / obj['yesterdayNav'] * 100

    navList[-1]['yesterdayNav'] = 0
    navList[-1]['navA'] = 0
    navList[-1]['navRate'] = 0

    saveToFile(symbol, navList)
    #return navList


def saveToFile(symbol, content):
   fobj = open(symbol + '.json', 'a', encoding="utf-8")
   fobj.write(str(content))
   fobj.close


getFundNavBatch('005636')
