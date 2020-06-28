#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 东方财富股票数据获取

import os
import demjson
import re
import requests


from pyquery import PyQuery as pq

import storage

DS = os.path.basename(__file__)

# 获取日 K 数据
# 数据格式：date, 今开，今收，最高，最低，成交量，成交额，振幅
# 参数
# id：股票代码
# type：
# rtntype：
# 时分数据：type=r，rtntype=5
# 盘前时分数据：iscr=true, type=r, rtntype=5
# 5日数据 ：type=t5k，rtntype=5
# 日k     ：type=k，rtntype=6
# 周k     ：type=wk，rtntype=6
# 月k     ：type=mk，rtntype=6
 
keys = ['date', 'open', 'close', 'high', 'low', 'volume', 'amount']
K_LINE_URL = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?token=4f1862fc3b5e77c150a2b985b12db0fd&authorityType=fa&cb='

def test_dynamic(arg):
    print(arg)

'''
获取盘前时分数据
'''
def getCRTicketData(symbol):
    r = requests.get(K_LINE_URL, params = {'id': symbol, 'type': 'r', 'rtntype': 5, 'iscr': 'true'})
    data = re.sub(r'^[\w\W]*\(', '', r.text)
    data = re.sub(r'\)[\w\W]*$', '', data)
    data = demjson.decode(data)
    
    storage.save_to_file(DS, 'stock', 'tick', symbol, data['name'], data)

    ret = {
        'code': data['code'],
        'historyData': []
    }

    for item in data['data']:
        ret['historyData'].append(dict(zip(['date', 'price', 'volume'], re.split('\s*,\s*', item))))

    return ret
#print(getCRTicketData('6001151'))

'''
获取日K线图数据
'''
def getDayKData(symbol):
    r = requests.get(K_LINE_URL, params = {'id': symbol, 'type': 'k', 'rtntype': 6})
    data = re.sub(r'^[\w\W]*\(', '', r.text)
    data = re.sub(r'\)[\w\W]*$', '', data)
    data = demjson.decode(data)

    ret = {
        'name': data['name'],
        'code': data['code'],
        'historyData': []
    }

    # "data": [
    #     "2007-03-01,18.16,16.55,18.64,16.06,1977634,9500302848,-"
    #]
    for item in data['data']:
        ret['historyData'].append(dict(zip(keys, re.split('\s*,\s*', item))))
  
    if len(ret['historyData']) > 0:
        ret['listingDate'] = ret['historyData'][0]['date']

    return ret
   

#print(getDayKData('6013181'))

'''
获取周K线图数据
'''
def getWeekKData(symbol):
    r = requests.get(K_LINE_URL, params = {'id': sybmol, 'type': 'wk', 'rtntype': 6})
    data = re.sub(r'^[\w\W]*\(', '', r.text)
    data = re.sub(r'\)[\w\W]*$', '', data)
    data = demjson.decode(data)

    ret = {
        'name': data['name'],
        'code': data['code'],
        'historyData': []
    }

    # "data": [
    #     "2007-03-01,18.16,16.55,18.64,16.06,1977634,9500302848,-"
    #]
    for item in data['data']:
        ret['historyData'].append(dict(zip(keys, re.split('\s*,\s*', item))))

    if len(ret['historyData']) > 0:
        ret['listingDate'] = ret['historyData'][0]['date']

    return ret







'''
获取K线图数据
'''
def getKLineData(symbol, t, rtntype, iscr=False):
    params = {'id': symbol, 'type': t, 'rtntype': rtntype}
    if t == 'r':
        # 是否为盘前时分数据
        params['iscr'] = iscr

    r = requests.get(DAY_K_URL, params = params)
    data = re.sub(r'^[\w\W]*\(', '', r.text)
    data = re.sub(r'\)[\w\W]*$', '', data)
    data = demjson.decode(data)

    ret = {
        'name': data['name'],
        'code': data['code'],
        'historyData': []
    }

    # "data": [
    #     "2007-03-01,18.16,16.55,18.64,16.06,1977634,9500302848,-"
    #]
    for item in data['data']:
        ret['historyData'].append(dict(zip(keys, re.split('\s*,\s*', item))))

    if len(ret['historyData']) > 0:
        ret['listingDate'] = ret['historyData'][0]['date']

    return ret


'''
获取历史股票列表
股票列表在页面的显示格式：name(code)
'''
STOCK_LIST_URL = 'http://quote.eastmoney.com/stock_list.html'
def getStockList():
    r = requests.get(STOCK_LIST_URL)
    html = pq(r.content.decode('gbk').encode('utf-8', "ignore").decode('utf-8', 'ignore'))
    sh_ul = html('#quotesearch').find("ul").eq(0)
    sz_ul = html('#quotesearch').find('ul').eq(1)
    # 中国平安(1234566) 贵州茅台(234566) ...
    sh_stock_text = sh_ul.find('li').text()
    sz_stock_text = sz_ul.find('li').text()

    # 中国平安#123456#sh 贵州茅台#234566#sh
    stock_text = re.sub(r'\)', '#sh', re.sub(r'\(', '#', sh_stock_text))
    stock_text += ' ' + re.sub(r'\)', '#sz', re.sub(r'\(', '#', sz_stock_text))

    stock_list = re.split(r'\s+', stock_text)

    ret_list = []
    for stock in stock_list:
        l = re.split(r'#', stock)
        ret_list.append(dict(zip(['name', 'code', 'exchange'], l)))
    
    return ret_list

'''
获取新股列表
这个接口获取的其实是历史新股上市记录，该接口每天调一次，按时间排序取最近的50条数据

url参数说明：
type: XGSG_LB
st: 排序字段
ps: 一次返回多少条数据
'''
NEW_STOCK_URL = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=XGSG_LB&token=70f12f2f4f091e459a279469fe49eca5&st=listingdate,securitycode&sr=-1&p=1&ps=50&js={pages:(tp),data:(x)}&rt=53027454'
def getNewStockList():
    r = requests.get(NEW_STOCK_URL)
    d = demjson.decode(r.text)  #r.content.decode('gbk').encode('utf-8', 'ignore').decode('utf-8', 'ignore')
    
    ret_list = []
    for j in d['data']:
        ret_list.append({
            'code': j['securitycode'],
            'name': j['securityshortname'],
            'exchange': j['sc'],
            'listingDate': j['listingdate'][:10]
        })
    return ret_list

#print(getNewStockList())



#print(__name__)
#print(__package__)
