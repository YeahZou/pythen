# -*- coding: utf-8 -*-

# 日志集中处理

import logging
import logging.config

logging.config.fileConfig('logging.conf')

def getLogger(logger):
    return logging.getLogger(logger)
