#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
from test_storage import StorageTest

if __name__ == '__main__':
    suite = unittest.TestSuite()

    tests = [StorageTest("test_save_stock_industry_data"), StorageTest("test_read_stock_industry_data")]
    suite.addTests(tests)
    suite.addTest(StorageTest("test_save_stock_realtime_data"))
    suite.addTest(StorageTest("test_read_stock_realtime_data"))

    runner = unittest.TextTestRunner(verbosity = 2)
    runner.run(suite)
