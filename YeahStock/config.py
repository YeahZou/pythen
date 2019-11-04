# -*- coding:utf-8 -*-
"""
配置文件
"""

# 抓取数据相关接口
URL = {
    'Sina': {
        # 获取新浪行业数据接口
        'Industry': 'http://vip.stock.finance.sina.com.cn/q/view/newSinaHy.php',
        # 获取指定行业所有上市公司接口
        'StockOfIndustry': 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData',
        # 实时数据接口
        'RealTime': 'https://hq.sinajs.cn/etag.php',
        # K 线图数据
        'KLine': 'http://quotes.sina.cn/cn/api/jsonp.php/$cb/KC_MarketDataService.getKLineData'
    },
    'Sse': {
        # 日线
        'DayLine': 'http://yunhq.sse.com.cn:32041/v1/sh1/line/{code}?callback=&begin=0&end=-1&select=time%2Cprice%2Cvolume',
        # 实时数据
        'Tick': 'http://yunhq.sse.com.cn:32041/v1/sh1/list/self/{code}?callback=&select=last%2Copen%2Cname%2Chigh%2Clow%2Cchange%2Cchg_rate%2Cprev_close%2Cvolume%2Camount%2Ctradephase'
    },
    # 深交所 数据相关url
    'Szse': {
        # 日线
        'Tick': 'http://www.szse.cn/api/market/ssjjhq/getTimeData?marketId=1&code={code}',
        'DayLine': 'http://www.szse.cn/api/market/ssjjhq/getHistoryData?cycleType=32&marketId=1&code={code}',
        'WeekLine': 'http://www.szse.cn/api/market/ssjjhq/getHistoryData?cycleType=33&marketId=1&code={code}',
        'MonthLine': 'http://www.szse.cn/api/market/ssjjhq/getHistoryData?cycleType=34&marketId=1&code={code}'
    }
}
