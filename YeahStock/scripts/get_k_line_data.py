#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import importlib

import argparse
import requests

from yeahstock.logger import Logger

logger = Logger.getLogger(sys.argv[0])

def main():
    p = argparse.ArgumentParser(description="Crawl stock K-line data.")
    p.add_argument(
        '-DS',
        '--datasource',
        help='data source, 数据源，支持东方财富，新浪，上交所，深交所，同花顺',
        choices=['eastmoney', 'sina', 'sse', 'szse', 'tonghuashun'],
        required=True
    )
    p.add_argument(
        '-T',
        '--type',
        help='data type, support CRTicket(带盘前交易的时分数据), t5k(5日数据), DayK(日K), WeekK(周K), MonthK(月K)',
        choices=['CRTicket', 't5k', 'DayK', 'WeekK', 'MonthK'],
        required=True
    )

    args = p.parse_args()
    logger.info("data source is %s", args.datasource)
    mod = importlib.import_module('yeahstock.datasource.' + args.datasource)
    func = getattr(mod, 'get' + args.type + 'Data')
    logger.info('function name is %s', func)
    
    logger.info(func('600776'))

main()
