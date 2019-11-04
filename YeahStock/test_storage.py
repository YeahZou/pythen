#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import unittest
import io
import sys
import shutil
import glob

from storage import *
"""
单元测试类必须继承 unittest.TestCase 类
注意有返回值的方法和无返回值的方法的测试方式，
有返回值的测试可以用 assert* 方法，没有返回值的，如果要测试 print 的输出，可以将sys.stdout临时重定向到 StringIO
"""
class StorageTest(unittest.TestCase):
    """
    # 每个case执行前都会先执行此方法，用于做测试前的准备工作
    def setUp(self):
        print("Set up env for case")

    # 每个case执行完成后都会执行此方法，执行清理工作
    def tearDown(self):
        paths = glob.glob('data/*')
        for path in paths:
            shutil.rmtree(path)
        print("INFO: remove path ", paths)
    """

    # 所有 case 执行前准备一次环境
    @classmethod
    def setUpClass(cls):
        print("This %s method is called only once." % 'setUpClass')

    # 所有 case 执行后清理一次环境
    @classmethod
    def tearDownClass(cls):
        paths = glob.glob('data/*')
        for path in paths:
            shutil.rmtree(path)
        if (len(paths) > 0):
            print('remove paths ', paths)

    # 测试用例，以 test 开头
    def test_save_stock_industry_data(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        save_stock_industry_data('sina', 'industry_list.txt', '1234')
        sys.stdout = sys.__stdout__
        print('Captured:', captured_output.getvalue())

    def test_save_stock_realtime_data(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        save_stock_realtime_data('sz600123', 'this is a test')
        sys.stdout = sys.__stdout__
        print('Captured:', captured_output.getvalue())

    def test_read_stock_industry_data(self):
        self.assertEqual(read_stock_industry_data('sina', 'industry_list.txt'), '1234')

    def test_read_stock_realtime_data(self):
        self.assertEqual(read_stock_realtime_data('sz600123'), 'this is a test')

if __name__ == '__main__':
    unittest.main();
