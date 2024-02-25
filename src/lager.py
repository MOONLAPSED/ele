import os
import sys
import threading
from datetime import datetime, date
from time import sleep
import logging
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler, QueueHandler, QueueListener, HTTPHandler
from dotenv import load_dotenv
import json

"""
The Lager class provides centralized logging configuration and management for your Python application.

**Key Features**

* **Flexible Configuration:**
    * Supports log levels controlled by environment variables (D_LOGGER, I_LOGGER, etc.)
    * Handlers can be defined as file paths, HTTP endpoints, or queues.
* **Standard Logging:** Configures the root logger and provides methods to retrieve loggers
* **dictConfig Compatibility:**  Use the `from_config` method to load logging configuration directly from a dictionary (JSON or YAML format).

**Environment Variables**

The following environment variables control log levels and handlers:

* **D_LOGGER, I_LOGGER, W_LOGGER, E_LOGGER, C_LOGGER:**
    * **None:**  Do not add a level-specific handler; inherit from the parent logger.
    * **File Path (e.g., 'logs/errors.log'):** Create a rotating file handler.
    * **HTTP Address (e.g., 'https://logs.example.com/api'):** Create an HTTP handler.  
    * **Queue Name (e.g., 'log_queue'):** Create a queue handler (requires other parts of your application to set up the queue).

**Handler Specifications**
Handlers in environment variables are specified as comma-separated values with the following format:
   `handler_type:arg1:arg2:...`

Example: 
   `I_LOGGER=file:/var/log/app.log,http://localhost:5000/log` creates a file handler and an HTTP handler for info-level logs.
"""

"""D, I, W, E, C defined as either None, a path for a rotating file, or a path for a queue, or an adress for an http server. If None; does not propagate to the next level - uses the default logger. 
If a path; logs to a file. If a queue; logs to a queue. If an adress; logs to an http server. """

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,  
    'formatters': {
        'default': {
            'format': '[%(levelname)s]%(asctime)s||%(name)s: %(message)s',
            'datefmt': '%Y-%m-%d~%H:%M:%S%z'
        },
    },
    'handlers': {
        'console': {
            'level': logging.INFO,
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'level': logging.INFO,
            'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs', 'app.log')),
            'maxBytes': 10485760,  # 10MB 
            'backupCount': 10
        }
    },
    'root': {
        'level': logging.INFO,
        'propagate': True,
        'handlers': ['console', 'file']
    }
}


class Lager:
    _lock = threading.Lock()
    root_logger = None
    LOGGING_CONFIG = LOGGING_CONFIG

    @classmethod
    def get_logger(cls):
        """Retrieves the configured root logger.

        Returns:
            logging.Logger: The root logger instance.
        """
        with cls._lock:
            if cls.root_logger is None:
                logging.config.dictConfig(cls.LOGGING_CONFIG)
                cls.root_logger = logging.getLogger()
        return cls.root_logger

    @classmethod
    def branch_logger(cls, name):
        """Creates a child logger with the specified name.

        Args:
            name (str): Name of the child logger.

        Returns:
            logging.Logger: The child logger instance.
        """
        branch = '.'.join([cls.root_logger.name, name])
        return logging.getLogger(branch)

    @classmethod
    def get_logger_from_name(cls, name):
        """Retrieves a logger by its name.

        Args:
            name (str): The name of the logger.

        Returns:
            logging.Logger:  The logger instance.
        """
        return cls.get_logger().getChild(name)

 
    @classmethod
    def from_config(cls, config_file):
        """Loads logging configuration from a file.

        Args: 
            config_file (str): Path to the configuration file (JSON or YAML). 
        """
        with open(config_file) as f:
            config_dict = json.load(f)
        logging.config.dictConfig(config_dict)
        cls.root_logger = logging.getLogger()
        return cls()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.root_logger}, level={self.root_logger.level})"

    @classmethod
    def validate(cls):
        """Validates and updates the logging configuration based on environment variables."""

        for level, env_var_name in zip(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                                        ['D_LOGGER', 'I_LOGGER', 'W_LOGGER', 'E_LOGGER', 'C_LOGGER']):
            handler_config = os.getenv(env_var_name)
            if handler_config:
                handlers = []
                for handler_spec in handler_config.split(','):
                    handler_type, *handler_args = handler_spec.split(':')
                    if handler_type == 'file':
                        handlers.append({
                            'class': 'logging.handlers.RotatingFileHandler',
                            'filename': handler_args[0],
                            'maxBytes': 10*1024*1024,  # 10MB 
                            'backupCount': 5,
                            'formatter': 'standard'
                        })
                    elif handler_type == 'http':
                        handlers.append({
                            'class': 'logging.handlers.HTTPHandler',
                            'host': handler_args[0],
                            'url': handler_args[1],  # Assuming URL is the second arg
                            'method': 'POST',
                            'formatter': 'standard'
                        })
                    elif handler_type == 'queue':
                        handlers.append({
                            'class': 'logging.handlers.QueueHandler',
                            'queue': LOGGING_CONFIG['handlers']['queue']['queue']  
                        })
                    else:
                        print(f"Unknown handler type: {handler_type}") 

                if handlers:
                    handler_name = f'{level.lower()}_handler'
                    LOGGING_CONFIG['handlers'][handler_name] = handlers
                    LOGGING_CONFIG['loggers']['myapp']['handlers'].append(handler_name)

if __name__ == "__main__":
    lager = Lager()
