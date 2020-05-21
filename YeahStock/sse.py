#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 上交所数据采集

import requests
import re

import config

# 通过股票代码获取日线数据
# http://yunhq.sse.com.cn:32041/v1/sh1/line/600055?callback=&begin=0&end=-1&select=time%2Cprice%2Cvolume
# 返回值中的line: time，price，volume
def getDayLineByCode(code):
    url = config.URL['Sse']['DayLine'].format(code = code)
    #print(url)
    r = requests.get(url)
    # 去掉开头、结尾的括号
    d = r.text[1:-1]
    #print(d)

# 通过股票代码获取实时数据
# http://yunhq.sse.com.cn:32041/v1/sh1/list/self/600055?callback=&select=last%2Copen%2Cname%2Chigh%2Clow%2Cchange%2Cchg_rate%2Cprev_close%2Cvolume%2Camount%2Ctradephase
# 返回值中的 list: last、open、name、high、low、change、chg_rate、prev_close、volume、amount、tradephase
def getTickData(code):
    url = config.URL['Sse']['Tick'].format(code = code)
    r = requests.get(url)
    d = r.content.decode('gb2312', 'ignore').encode('utf-8', 'ignore').decode('utf-8', 'ignore')
    d = d[1:-1]
    #print(d)



