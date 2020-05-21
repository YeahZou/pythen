#!/usr/bin/env python

import re
import requests
import demjson

# 获取新成立的、处在认购期、可购买的基金列表
NEW_FUND_URL='http://fund.eastmoney.com/data/FundNewIssue.aspx?t=zs&sort=jzrgq,desc&isbuy=1&v=0.6485227866381129'
fundKeys = ['symbol', 'name', 'comapnyName', 'companyId', 'type', 'buyTime', 'rate', 'managerName', '', '', '','','managerId']
def getNewFundList(currentPage = 1, pageSize = 50):
    r = requests.get(NEW_FUND_URL, params={'page': str(currentPage) + ',' + str(pageSize)})
    data = re.sub(r'^[\w\W]+\{', '{', r.text)
    data = demjson.decode(data)

    fundList = []
    for fundValues in data['datas']:
        fundList.append(dict(zip(fundKeys, fundValues)))

    if data['curpage'] < data['pages']:
        fundList.extend(getNewFundList(currentPage + 1))

    return fundList



print(getNewFundList())
