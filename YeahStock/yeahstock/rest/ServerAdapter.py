#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import requests

from yeahstock.logger import Logger

BASE_URL = 'http://192.168.0.107:8080/yeahstock/stock/'
API_MAP = {
    'addStocks': 'addStocks'
}

logger = Logger.getLogger()

def addStocks(stocks = [], needCheck = False):
    '''将股票列表存入数据库
    :param stocks: 股票列表
    :type stocks: list
    :param needCheck: 保存前是否检查数据存在，默认不检查
    :type boolean
    :returns 保存成功返回 status = OK
    :rtype dict
    '''
    if len(stocks) == 0:
        logger.info("stock list is empty, nothing to do.")
        return

    ret = requests.post(BASE_URL + API_MAP['addStocks'], json = {'stockList': stocks, needCheck: needCheck})
    if ret.status_code != 200 or ret.json()['status'] != 'OK':
        func = sys._getframe().f_code.co_name
        logger.error("%s, save stocks failed, %s", func, ret.text)
        exit()

