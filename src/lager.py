import logging
from logging.config import dictConfig
import os
import sys
import threading
from logging.handlers import RotatingFileHandler, QueueHandler, QueueListener, HTTPHandler
from dotenv import load_dotenv

# load_dotenv() this will already have been called by the setup.py file but there is a possible entry point here.
def entry_point():
    """This function is called by the setup.py file to set up the logger. It is not called by the main program."""
    setup_logger()


class customlog(ABC):
    """This is an abstract class that is used to define the logger. It is not called by the main program."""
    def __static__init__(self):
        """Static logger to run only once."""
        if not hasattr(customlog, "init"):
            customlog.init = True
            self.logger.addHandler(self.handler)
            self.logger.propagate= False
    def __init__(self, logger, level, formatter, handler):
        self.logger= logger
        self.level= level
        self.formatter= formatter
        self.handler= handler
        self.logger.setLevel(self.level)
        self.handler.setLevel(self.level)
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        self.logger.propagate= False
        __static__init__()
    """D, I, W, E, C defined as either None, a path for a rotating file, or a path for a queue, or an adress for an http server. If None; does not propagate to the next level - uses the default logger. 
    If a path; logs to a file. If a queue; logs to a queue. If an adress; logs to an http server. """
    debug= os.getenv(D_LOGGER)
    info= os.getenv(I_LOGGER)
    warning= os.getenv(W_LOGGER)
    error= os.getenv(E_LOGGER)
    critical= os.getenv(C_LOGGER)