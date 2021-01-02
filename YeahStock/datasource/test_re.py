#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re

string = "<a href='http://www.szse.cn/certificate/individual/index.html?code=000027' target='_blank'><u>深圳能源</u></a>"
m = re.match(r'.+\<u\>\s*(.+)\s*\<u\>', string)
print(m.group(1))
