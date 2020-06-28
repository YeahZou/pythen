#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import requests

http = requests.Session()

def print_res(r, *args, ** kwargs):
    print(r.text)

http.hooks['response'] = [print_res]

requests['get']('http://quote.eastmoney.com/stock_list.html')


