#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import logging
import time
import re
import sys
import demjson
import math

# type2 = 0 基金类型为"全部"
FUND_LIST_URL = 'http://vip.stock.finance.sina.com.cn/fund_center/data/jsonp.php/((/NetValue_Service.getNetValueOpen?sort=nav_date&asc=0&type2=0'

# 获取基金历史净值 url
FUND_HISTORY_NAV_URL = 'https://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?callback=(('

# 字段映射关系
keyMaps = {
    'sname': 'name',
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
#####################################################################################################
#####################################################################################################
# get one page fund list
def getOnePageFund(page, pageNum):
    r = requests.get(FUND_LIST_URL, params={'page': page, 'num': pageNum})
    data = r.content.decode('gbk').encode('utf-8', "ignore").decode('utf-8', 'ignore')
    data = re.sub('^[\s\S]+?\\{', '{', data)
    data = re.sub('\\}\\)[\s\S]+?$', '}', data)

    # 将 javascript 格式的 json 转为标准 json
    jsonData = demjson.decode(data, decode_object=convertKey)
    #print(jsonData)
    return {'totalNum': jsonData['total_num'], 'fundList': jsonData['data']}

# get all fund list
def getAllFundList(pageNum = 40):
    fundList = []
    onePageFund = getOnePageFund(1, pageNum)
    fundList.extend(onePageFund['fundList'])

    pageCount = math.ceil(onePageFund['totalNum'] / pageNum)
    
    if pageCount > 1:
        for page in range(2, pageCount + 1):
            onePageFund = getOnePageFund(page, pageNum)
            fundList.extend(onePageFund['fundList'])
    
    saveToFile('fundList.json', fundList)


def convertKey(obj):
    for k in keyMaps.keys():
        if k in obj.keys():
            obj[keyMaps[k]] = obj[k]
            del obj[k]
    return obj

#getFundList()

#######################################################################################################
#######################################################################################################
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

# get a fund history nav data
def getOneFundNavBatch(symbol):
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

#############################################################################
#############################################################################

FUND_BASIC_INFO_URL = 'https://stock.finance.sina.com.cn/fundInfo/api/openapi.php/FundPageInfoService.tabjjgk?format=json&callback=fund'

# 根据基金代码获取基金基本信息
def getFundBasicInfo(symbol):
    r = requests.get(FUND_BASIC_INFO_URL, params = {'symbol': symbol})
    # remove '\/', otherwise has warning: DeprecationWarning: invalid escape sequence '\/' 
    data = re.sub(r'\\\/', '', r.text)
    data = re.sub(r'\\"', "'", data)
    data = data.encode('utf-8', 'ignore').decode('unicode-escape')
    data = re.sub(r'^[\w\W]+fund\(', '', data)
    data = re.sub(r'\)$', '', data)
    data = re.sub(r'[\n\r]', '', data)
    dictData = demjson.decode(data, decode_object=convertBasicInfo)

    dictData['result']['data']['symbol'] = symbol
    return dictData['result']['data']
    #print(dictData)


def convertBasicInfo(obj):
    if 'symbol' in obj.keys():
        ret = {}

        ret['name'] = obj['jjjc']
        ret['fullName'] = obj['jjqc']
        ret['issueDate'] = obj['clrq'][:10]
        ret['type'] = obj['Type2Name']
        ret['companyId'] = obj['CompanyId']
        ret['companyName'] = obj['glr']

        mList = re.findall(r'mid\=(\d+)', obj['ManagerName'])
        mmList = re.findall(r'\>(.+?)\<a\>', obj['ManagerName'])
        ret['mamagerId'] = ','.join(mList)
        ret['managerName'] = ','.join(mmList)
        
        return ret
    return obj

print(getFundBasicInfo('005636'))
##############################################################################
##############################################################################
# save to file
def saveToFile(symbol, content):
   fobj = open(symbol + '.json', 'w', encoding="utf-8")
   fobj.write(str(content))
   fobj.close

###############################################################################
###############################################################################

FUND_DOMAIN = 'localhost:8080/yeahstock/fund/'
API_MAP = {
    'addFund': 'addFund',
    'saveFundNav': 'saveFundNav'
}
# rest method, save data to database
def addFund(fund):
    url = FUND_DOMAIN + API_MAP['addFund']
    r = requests.post(url, data = fund)

    print(r.text)

#getOnePageFund(1, 20)
#getAllFundList()
#getOneFundNavBatch('005636')
