#!/usr/bin/env python
# -*- coding: utf-8 -*-


import storage
import sina

def save_industry_data():
    industry_list = sina.get_industry_list()
    storage.save_stock_industry_data('sina', 'industry.txt', str(industry_list))



if __name__ == '__main__':
    save_industry_data()
