#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
新浪财经网站获取股票信息相关方法

该模块仅获取数据、进行简单的加工，返回值都是字符串
"""
import requests
import logging
import time
import re
import sys
import json

import config

logging.basicConfig(level = logging.ERROR, format = '[%(name)s] [%(levelname)s] [%(asctime)s]: %(message)s ')
logger = logging.getLogger(sys.argv[0])


#INDUSTRY_TYPE_URL = 'http://vip.stock.finance.sina.com.cn/q/view/newSinaHy.php'
#indu_url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData'

# 获取新浪行业列表
# 请求示例：
# http://vip.stock.finance.sina.com.cn/q/view/newSinaHy.php
# 参数说明：新浪行业url，未给定则从config中获取
# 数据格式：
# var S_Finance_bankuai_sinaindustry = {"new_blhy":"new_blhy,玻璃行业,19,9.0773684210526,-0.03,-0.32940360610264,137067530,1003694068,sh601636,2.186,3.740,0.080,旗滨集团", ...}
# 返回数据说明：
# 行业拼音，行业名称，公司家数，平均价格，涨跌额，涨跌幅度（%），总成交量（手），总成交额（万元），领涨股，涨幅，当前价格，涨跌额，领涨股名称 
def get_industry_list():
    url = config.URL['Sina']['Industry']
    r = requests.get(url)
    #print(r.apparent_encoding)
    #r.encoding='gb2312'
    industry_list = []
    if r.status_code != 200:
        logger.error('get industry type data failed.')
    else:
        keys = ['namePY', 'name', 'companyCount', 'avgPrice', 'changeAmount', 'changeRate', 'volume', 'turnover', 'leader', 'leaderRise', 'leaderCurrentPrice', 'leaderChangeAmount', 'leaderName']
        data = r.content.decode('gb2312').encode('utf-8', "ignore").decode('utf-8', 'ignore')
        data = re.sub(r'^.+?{', '{', data)
        #print(data)
        j = json.loads(data)
        for (k, v) in j.items():
            values = re.split(r'\s*,\s*', v)
            industry = dict(zip(keys, values))
            industry_list.append(industry)
    return industry_list


# http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData
# 获取行业分类名称获取所有股票
# 输入：行业名称
# 输出：[{"symbol": "sh600002", "code": "600002", "name": "华东医疗"}, {...}]

def get_stocks_of_industry(industry):
    url = config.URL['Sina']['StockOfIndustry']
    args = {'page': 1, 'num': 40, 'sort': 'symbol', 'asc': 1, 'node': industry, '_s_r_a': 'init'}
    r = requests.get(url, params = args)
    t = r.content.decode('gb2312').encode('utf-8', 'ignore').decode('utf-8', 'ignore')
    # 返回值不是正真的json格式
    dict_list = re.split(r'},{', re.sub('^\[\{|\}\]$', '', t))
    stocks_of_indu = []
    for str_v in dict_list:
        re_obj = re.match(r'symbol:"(?P<symbol>.+?)".+?code:"(?P<code>\d+)".+?name:"(?P<name>.+?)".+', str_v)
        if re_obj:
            stocks_of_indu.append(re_obj.groupdict())
    return stocks_of_indu
#    print(stocks_of_indu)


#REAL_DATA_URL = 'https://hq.sinajs.cn/etag.php'

#keys = ['name', 'todayOpen', 'yestodayClose', 'real', 'max', 'min', 'avg', 'real', 'volume', 'turnover', '', '', '', ]
# 获取实时数据
# 请求示例：
# https://hq.sinajs.cn/etag.php?_=1565536469657&list=sh600055
# 数据格式：
# var hq_str_sh600055="万东医疗,9.620,9.610,9.710,9.720,9.560,9.700,9.710,3212246,31056145.000,15400,9.700,35200,9.690,96000,9.680,49204,9.670,1500,9.650,9200,9.710,32700,9.720,47400,9.730,26800,9.740,30300,9.750,2019-08-09,15:00:00,00,";
def get_real_time_data_by_code(code):
    url = config.URL['Sina']['RealTime']
    r = requests.get(url, params={'_': int(round( time.time() * 1000)), 'list': code})
    res = ''
    if r.status_code != 200:
        logger.error('get real data failed.')
    else:
        logger.info('code is %(code)s, data is %(data)s' % {'code': code, 'data': r.text})
        # 去掉js变量申明
        res = re.sub(r'^[^=]+="', '', r.text)
        # 去掉结尾换行符
        res = re.sub(r',?";\n?$', '', res)
        # 转为数组
        res = re.split('\s*,\s*', res)

        logger.debug('split result is %(res)s' % {'res' : res})
    return res


# test
#get_real_time_data_by_code('sh600055');


# 获取K线图数据
# 请求示例：
# http://quotes.sina.cn/cn/api/jsonp.php/$cb/KC_MarketDataService.getKLineData?symbol=sh600008
# 数据格式：
# /*<script>location.href='//sina.com';</script>*/
# $cb([{"d":"2000-04-27","o":"18.000","h":"18.550","l":"16.010","c":"17.420","v":"68952800","pv":null,"pa":null},...]);
#K_LINE_URL = 'http://quotes.sina.cn/cn/api/jsonp.php/$cb/KC_MarketDataService.getKLineData'
def get_k_line_data_by_symbol(symbol):
    url = config.URL['Sina']['KLine']
    r = requests.get(url, params={'symbol': symbol})
    res = ''
    if r.status_code != 200:
        logger.error('get k_line data failed. response is: ' + r.text)
    else:
        #logger.debug('symbol: %(symbol)s, data is %(data)s' % {'symbol': symbol, 'data': r.text})
        # 去掉js注释
        # res = re.sub(r'/\*.*\*/', '', r.text)
        # 去掉数据前后的字符
        res = re.sub(r'^[\w\W]+?\[', '[', r.text)
        res = re.sub(r'\);$', '', res)
        # 把null转为""
        res = re.sub(r'null', '""', res)

        logger.debug(res);
        format_data = format_k_line_data(res)
        logger.debug('formated data: %(data)s' % {'data': json.dumps(format_data)})
    return res

def format_k_line_data(data_str):
    data_arr = json.loads(data_str)
    format_data = []
    for elem in data_arr:
        felem = {
            'date': elem['d'],
            'open': elem['o'],
            'high': elem['l'],
            'low': elem['l'],
            'close': elem['c'],
            'volume':elem['v']
        }
        format_data.append(felem)
    
    return format_data

#get_k_line_data_by_symbol('sh600055');
