# -*- coding: utf-8 -*-

"""
 日志集中处理
"""
from os import path
import sys
import logging
import logging.config

from os import path
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path)

#print("log file path: " + log_file_path)
#logging.config.fileConfig('.logging.conf')

def getLogger(logger = None):
    if logger == None:
        f_back = sys._getframe().f_back
        fname = f_back.f_code.co_filename
        funcname = f_back.f_code.co_name
        lineno = f_back.f_lineno

        logger = "{}:{}:{}".format(fname, funcname, lineno)
    return logging.getLogger(logger)
