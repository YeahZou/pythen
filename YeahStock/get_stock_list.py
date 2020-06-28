#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests

from lib import ds_eastmoney as em
from lib import rest

def main():
    p = argparse.ArgumentParser()
    p.add_argument('-H', '--history', help='get history stock list, default just get new stocks', action='store_true')

    args = p.parse_args()

    stocks = []
    if args.history:
        stocks = em.getStockList()
    else:
        stocks = em.getNewStockList()
    
    #print(stocks)
    rest.saveStockList(stocks[0])


main()
