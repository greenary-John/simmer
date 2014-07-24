'''Logger
This is a file containing the Logger class which defines a Logger object.
This Logger object has different methods all used to write to the simmer.log
file contained in the simmer directory. This allows users to have a record of
program output and debugging information (usually just what step the program
is on and when) in a file as opposed to temporarily printing it to the Terminal
to be lost after use.

Author: Patrick Osterhaus   s-osterh
'''
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
    
