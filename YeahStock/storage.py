#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 处理数据的本地存储


import datetime
import os
import sys
import re

ROOT_PATH = 'data'

def getpath(strategy):
    d = datetime.date.today()
    year, month = str(d.year), str(d.month).zfill(2)

    return os.path.join(ROOT_PATH, strategy, year, month) 

"""
获取股票行业的存储目录
参数: 
    strategy: 行业的分类依据，如 sina, sse

返回:
    行业数据的存储目录，如 data/stock/industry/201901/sina, data/stock/industry/201901/sse
"""
def get_stock_industry_path(strategy, d = datetime.date.today()):
    #d = datetime.date.today()
    datestr = str(d.year) + str(d.month).zfill(2)

    return os.path.join(ROOT_PATH, 'stock', 'industry', datestr, strategy)

"""
获取股票实时数据保存目录
"""
def get_stock_realtime_path(symbol, d = datetime.date.today()):
    #d = datetime.date.today()
    year, month, day = str(d.year), str(d.month).zfill(2), str(d.day).zfill(2)
    stock_type = re.sub(r'^[szh]+(\d{3})\d{3}$', '\g<1>', symbol)

    return os.path.join(ROOT_PATH, 'stock', 'realtime', year, month, day, stock_type)


def save_data(path, filename, data):
    if (not os.path.exists(path)):
        os.makedirs(path)
    f = os.path.join(path, filename)
    fobj = open(f, 'a', encoding="utf-8")
    fobj.write(data)
    fobj.close

"""
保存行业数据
参数：
   strategy: 行业分类依据
   filename: 文件名称
   data: 要保存的数据
"""
def save_stock_industry_data(strategy, filename, data):
    try:
        path = get_stock_industry_path(strategy)
        save(path, filename, data)
    except Exception as err:
        func = sys._getframe().f_code.co_name
        handle_except(func, err)
        # TODO: email notice
    

def save_stock_realtime_data(symbol, data):
    try:
        path = get_stock_realtime_path(symbol)
        filename = symbol + '.txt'
        save_data(path, filename, data)
    except Exception as err:
        func = sys._getframe().f_code.co_name
        handle_except(func, err)


def save_stock_dey_line_data(symbol, data):
    '''
    保存日线数据
    '''
    try:
        path = get_stock_day_line_path(symbol)
        if (not os.path.exists(path)):
            os.makedirs(path)

        filename = symbol + '.txt'
        f = os.path.join(path, 


"""
读取指定日期的股票行业数据，如果日期未指定，则读取当天的数据
"""
def read_stock_industry_data(strategy, filename, date = datetime.date.today()):
    try:
        path = get_stock_industry_path(strategy, date)
        f = os.path.join(path, filename)
        fobj = open(f, 'r', encoding="utf-8")

        content = fobj.read()
        fobj.close

        return content
    except Exception as err:
        func = sys._getframe().f_code.co_name
        handle_except(func, err)


"""
读取指定日期的股票实时数据
"""
def read_stock_realtime_data(symbol, date = datetime.date.today()):
    try:
        path = get_stock_realtime_path(symbol, date)
        filename = symbol + '.txt'
        f = os.path.join(path, filename)
        fobj = open(f, 'r', encoding="utf-8")
        content = fobj.read()
        fobj.close

        return content
    except Exception as err:
        func = sys._getframe().f_code.co_name
        handle_except(func, err)

# 异常处理
def handle_except(func, err):
    script = os.path.basename(__file__)
    print(script, func, err)

