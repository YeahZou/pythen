#!/usr/bin/env python
# -*- coding:utf-8 -*-

import importlib

import argparse
import requests

from lib import ds_eastmoney as em
from lib import rest

def main():
    p = argparse.ArgumentParser(description="Crawl stock K-line data.")
    p.add_argument(
        '-T',
        '--type',
        help='data type, support cr(带盘前交易的时分数据), t5k(5日数据), k(日K), wk(周K), mk(月K)',
        choices=['cr', 't5k', 'k', 'wk', 'mk'],
        required=True
    )

    args = p.parse_args()

    mod = importlib.import_module('ds_eastmoney', 'lib')
    func = getattr(mod, 'get' + args.type.upper() + 'Data')
    print(func)

main()
