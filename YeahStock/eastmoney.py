#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 东方财富股票数据获取

import demjson
import re
import requests

# 获取日 K 数据
# 数据格式：date, 今开，今收，最高，最低，成交量，成交额，振幅
# 参数
# id：股票代码
# type：
# rtntype：
# 时分数据：type=r，rtntype=5
# 5日数据 ：type=t5k，rtntype=5
# 日k     ：type=k，rtntype=6
# 周k     ：type=wk，rtntype=6
# 月k     ：type=mk，rtntype=6
 
keys = ['date', 'open', 'close', 'high', 'low', 'volume', 'amount']
DAY_K_URL = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?token=4f1862fc3b5e77c150a2b985b12db0fd&authorityType=fa&cb='

def getDayKData(symbol):
    r = requests.get(DAY_K_URL, params = {'id': symbol, 'type': 'k', 'rtntype': 6})
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
    
    return ret
   

print(getDayKData('6013181'))
