# -*- coding: utf-8 -*-

# 工具类

import re

REQUEST = {
    'headers': {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept - Encoding':'gzip, deflate',
        'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
        'Connection':'Keep-Alive',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
    }
}

def get_exchange_by_code(code = ''):
    ''' 根据股票代码判断所属交易所
        
    :param code: 股票代码
        (default is '')
    :type code: str
    :returns: sz, sh
    :rtype: str
    '''
    exchange = ''
    if re.match('^(300|000|002)', code):
        exchange = 'sz'
    elif re.match('^(688|600)', code):
        exchange = 'sh'

    return exchange

def get_market_by_code(code = ''):
    '''根据股票代码判断所属板块

    :param code: 股票代码
        (default is '')
    :type code: str
    :returns: main(主板), sme(中小板), nm(创业板), star(科创板)
    :rtype: str
    '''
    market = ''
    if re.match('^300', code):
        market = 'nm'
    elif re.match('^002', code):
        market = 'sme'
    elif re.match('^(000|600)', code):
        market = 'main'
    elif re.match('^688', code):
        market = 'star'
    
    return market

