#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

BASE_URL = 'http://192.168.31.69:8080/yeahstock/'

API_MAP = {
    'addStocks': 'stock/addStocks'
}

for api in API_MAP:
    API_MAP[api] = BASE_URL + API_MAP[api]

def saveStockList(stocks):
    if not isinstance(stocks, list):
        stocks = [stocks]
    
    res = requests.post(API_MAP['addStocks'], json={'stockList': stocks})
    print(res.text)
