#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据的格式化、清洗、存储
"""
import re
import json

import sina
import storage

def clean_industry_data():
    data = sina.get_industry_json()

    storage.save_stock_industry_data('sina', 'industry.txt', data)
    #print(data)


if __name__ == '__main__':
    clean_industry_data()
