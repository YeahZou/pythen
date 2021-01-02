
import sys
import logging
import logging.handlers

#logging.config.fileConfig('logging.conf')
#logger = logging.getLogger(sys.argv[0])

sys.path.append('..')
#import datasource.Logger as Logger
logger = logging.getLogger(sys.argv[0])

sh = logging.handlers.SMTPHandler(('smtp.qq.com', 25), '2544610309@qq.com', '2544610309@qq.com', 'This is a python send email test.', credentials=('2544610309@qq.com', 'meksbrlzyllhebdj'))

logger.addHandler(sh)

logger.info("This is logger info")
logger.debug("This is logger debug")
logger.error("This is logger error")


