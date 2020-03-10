#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import re

URL_LIST = '''
https://www.doutub.com/
https://www.jiuwa.net/
https://www.doutula.com/
https://mm.sayloving.com/biaoqing.html
http://www.dtzhuanjia.com/
http://www.dbbqb.com/
'''.strip().splitlines(False)

S_URL='''
https://api.doutub.com/api/bq/search
'''.strip().splitlines(False)


r = requests.get(S_URL[0], params={'keyword': '害怕'})
print(r.text)
j = r.json();
rows = j['data']['rows']
for row in rows:
    imgName = row['imgName']
    path = row['path']
    ir = requests.get(path)
    open(imgName + re.sub(r'^.+(\.(jpg|png|gif|bmp))$', '\g<1>', path, flags=re.IGNORECASE), 'wb').write(ir.content)

