
# -*- coding: UTF-8 -*-

# 新浪财经网站获取股票信息相关方法

import requests
import logging
import time
import re
import sys

logging.basicConfig(level = logging.DEBUG, format = '[%(name)s] [%(levelname)s] [%(asctime)s]: %(message)s ')
logger = logging.getLogger(sys.argv[0])

#console = logging.StreamHandler()
#console.setLevel(logging.INFO)

#logger = logging.getLogger("sina_log").addHandler(console)
#logger.setLevel(logging.INFO)

REAL_DATA_URL = 'https://hq.sinajs.cn/etag.php'
# request : https://hq.sinajs.cn/etag.php?_=1565536469657&list=sh600055
# return  : var hq_str_sh600055="万东医疗,9.620,9.610,9.710,9.720,9.560,9.700,9.710,3212246,31056145.000,15400,9.700,35200,9.690,96000,9.680,49204,9.670,1500,9.650,9200,9.710,32700,9.720,47400,9.730,26800,9.740,30300,9.750,2019-08-09,15:00:00,00,";

keys = ['name', 'today_open', 'yestoday_close', 'real', 'max', 'min', '', 'real', '', '成交额', '', '', '', ]
def get_real_time_data_by_code(code):
    r = requests.get(REAL_DATA_URL, params={'_': int(round( time.time() * 1000)), 'list': code})
    if r.status_code != 200:
        logger.error('get real data failed.')
    else:
        logger.info('code is %(code)s, data is %(data)s' % {'code': code, 'data': r.text})
        res = re.sub(r'^[^=]+="', '', r.text)
        res = re.sub(r',?";\n?$', '', res)
        res = re.split('\s*,\s*', res)

        logger.debug('split result is %(res)s' % {'res' : res})



# test
get_real_time_data_by_code('sh600055');
