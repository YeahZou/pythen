#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re

import config

# 获取实时数据
# http://www.szse.cn/api/market/ssjjhq/getTimeData?marketId=1&code=300311
def get_tick_data(code):
    url = config.URL['Szse']['Tick'].format(code = code)
    r = requests.get(url)


def get_day_line_data(code):

