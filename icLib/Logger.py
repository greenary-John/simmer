import logging
import os

class Logger(object):
    def __init__(self):
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',filename=os.path.abspath(os.path.join(os.path.dirname(__file__),"..","simmer.log")),level=logging.DEBUG)

    def debug(self,message):
        logging.debug(message)
    def info(self,message):
        logging.info(message)
    def warning(self,message):
        logging.warning(message)
    def error(self,message):
        logging.error(message)
    def critical(self,mesage):
        logging.critical(message)
    
