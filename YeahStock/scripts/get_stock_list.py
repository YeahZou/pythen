#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
获取股票列表
"""
import importlib
import pkgutil

import argparse
import requests

from yeahstock.logger import Logger
from yeahstock import datasource as ds
from yeahstock.config import settings

log = Logger.getLogger()

def main():
    p = argparse.ArgumentParser()
    p.add_argument('-H', '--history', help='获取历史股票列表，默认只获取最近上市的50条', action='store_true')
    p.add_argument('--dry-run', help='仅测试能否正常爬取数据，不入库', action='store_true')

    args = p.parse_args()

    if args.dry_run:
        settings.DRY_RUN = 1
    else:
        settings.DRY_RUN = 0

    func_name = 'getNewStockList'
    if args.history:
        func_name = 'getStockList'

    for importer, modname, ispkg in pkgutil.iter_modules(ds.__path__):
        module = importer.find_module(modname).load_module(modname)
        
        func = None
        if hasattr(module, func_name) and modname == 'eastmoney':
            func = getattr(module, func_name)
        if func != None:
            print(func_name, modname)
            func()
    
    #print(stocks)
   # rest.saveStockList(stocks[0])


main()
