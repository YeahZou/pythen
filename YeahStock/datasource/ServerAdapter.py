#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import requests

import Logger

BASE_URL = 'http://192.168.0.106:8080/yeahstock/stock/'
API_MAP = {
    'addStocks': 'addStocks'
}

logger = Logger.getLogger('ServerAdapter')

def addStocks(stocks = []):
    if len(stocks) == 0:
        logger.info("stock list is empty, nothing to do.")
        return

    ret = requests.post(BASE_URL + API_MAP['addStocks'], json = {'stockList': stocks})
    if ret.status_code != 200 or ret.json()['status'] != 'OK':
        func = sys._getframe().f_code.co_name
        logger.error("%s, save stocks failed, %s", func, ret.text)

