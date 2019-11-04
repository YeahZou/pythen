#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import requests
import re
import json

indu_type_url = 'http://vip.stock.finance.sina.com.cn/q/view/newSinaHy.php'
indu_url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData'

# 获取新浪行业列表
r = requests.get(indu_type_url)
if r.status_code != 200:
    print('get industry type data failed.')
else:
    ret = re.sub(r'^.+?{', '{', r.text)
    print(ret)
    j = json.loads(ret)
    # 新浪行业分类列表
    indu_list = []
    # 新浪行业分类名称列表
    indu_name_list = []
    for (k, v) in j.items():
        m_obj = re.search(r'^\w+,(.+?),', v)
        indu_list.append(k)
        indu_name_list.append(m_obj.group(1))
    #print(indu_name_list)
    #print(indu_list)

    # 获取一个行业的股票列表
    args = {'page': 1, 'num': 40, 'sort': 'symbol', 'asc': 1, 'node': indu_list[0], '_s_r_a': 'init'}
    #r = requests.get(indu_url, params = args)
    # 返回值不是正真的json格式
    dict_list = re.split(r'},{', re.sub('^\[\{|\}\]$', '', r.text))
    stocks_of_indu = []
    for str_v in dict_list:
        re_obj = re.match(r'symbol:"(?P<ex>[szh]{2})(?P<code>\d+).+?name:"(?P<name>.+?)".+', str_v)
        if re_obj:
            stocks_of_indu.append(re_obj.groupdict())
    print(stocks_of_indu)
