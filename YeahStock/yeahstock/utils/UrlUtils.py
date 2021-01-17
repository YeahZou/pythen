"""
URL 转换工具
"""

import re

em_k_line_url = 'http://65.push2his.eastmoney.com/api/qt/stock/kline/get?cb=&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&beg=0&end=20500101&smplmt=460&lmt=1000000&_=1610265367454'

em_stock_list_url = 'http://48.push2.eastmoney.com/api/qt/clist/get?cb=&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fs=m:1+t:23&fields=f12,f14,f26&_=1610793059494'

ths_stock_list_url = 'http://q.10jqka.com.cn/index/index/board/{}/field/zdf/order/desc/page/{}/ajax/1/'

def get_request_head():
    return {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept - Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection':'Keep-Alive',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
    }

def get_tonghuashun_stock_list_url(board, page):
    '''根据板块和页数返回同花顺获取股票列表url
        board
        page
    '''
    return ths_stock_list_url.format(board, page)

def get_eastmoney_kline_url(code = '', klt = 'dk', fqt = 'none', market = None):
    '''获取东方财富k线图url

    根据股票代码、k线图类型、复权类型、所属交易所，返回get请求的url
    '''

    secid = ''
    '''
    k线类型
    '''
    klt_map = {
        'dk': '101',
        'wk': '102',
        'mk': '103'
    }
    '''
    复权类型
    '''
    fqt_map = {
        'none': '0',
        'forward': '1',
        'backward': '2'    
    }

    if market == None:
        if re.match('^(300|000|002)', code):
            market = 'szse'
        elif re.match('^(688|600)', code):
            market = 'sse'

    if market == 'szse':
        secid = '0.' + code
    elif market == 'sse':
        secid = '1.' + code

    return em_k_line_url + '&secid={}&klt={}&fqt={}'.format(secid, klt_map[klt], fqt_map[fqt]) 

def get_eastmoney_stock_list_url(exchange = None, market = None):
    '''获取东方财富股票列表url
    根据交易所名称和所属板块，获取对应的url，返回get请求的url
    按上市日期降序排序

    注意：分页参数名称为pn,需要调用时附上
    '''
    return em_stock_list_url + '&fid=f26&po=1&fs=' + 'm:0 t:6,m:0 t:13,m:0 t:80,m:1 t:2,m:1 t:23'
    
def get_eastmoney_new_stock_list_url():
    '''获取东方财富新股列表url
    按上市日期降序排序

    注意：分页参数名称为pn，需要调用时附上
    '''
    return em_stock_list_url + '&fid=f26&po=1&fs=' + 'm:0 f:8,m:1 f:8'
