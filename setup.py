#!/usr/bin/env python

# setup.py-only functions, not for runtime or user-facing code
# +--------------------+ private setup.py-only funcs
# 1. __log_error__
# 2. __shell_error__
# 3. __starter__
# +--------------------+ setup.py-only funcs
# 4 __pipenv__
# 5 __mainpath__
# 6 SetupConfig/__entry_point__/pre-runtime-endpoint
# +--------------------+ Pydantic app and main. Global-scope functions.
# 7 BasedModel
# 8 main
# 9 ValidateAppsettings
# 10 BasedSettings
# 11 BasedApp
# 12 __main__/runtime(init --> main.py)


from datetime import datetime, date
from setuptools import setup, find_packages
import subprocess
import os
import sys
import logging
import logging.config

try:
    # Initialize setup logger for setup.py
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file_handler': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.abspath(os.path.join(os.path.dirname(__file__), 'logs', 'setup.log')),
                'maxBytes': 10*1024*1024,  # 10MB 
                'backupCount': 5,
                'formatter': 'standard'
            },
        },
        'formatters': {
            'standard': {
                'format': '[%(levelname)s]%(asctime)s||%(name)s: %(message)s',
                'datefmt': '%Y-%m-%d~%H:%M:%S%z'
            },
        },
        'root': {
            'level': logging.INFO,
            'handlers': ['file_handler']
        },
    }
    logging.config.dictConfig(logging_config)
except Exception as e:
    # Basic logging setup for setup.py
    log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'logs', 'setup.log'))
    logging.basicConfig(filename=log_file_path, level=logging.INFO)
    logging.error(f"Error setting up logging configuration: {e}")
    raise SystemExit(1)  # Indicate installation failure



def __mainpath() -> tuple:
    """Determines project paths, adjusts permissions, sets env variables."""

    project_root = os.path.abspath(os.path.dirname(__file__))
    os.environ['PROJECT_ROOT'] = project_root

    try:
        sts = os.stat(project_root)
        for root, dirs, files in os.walk(project_root):
            for d in dirs:
                os.chmod(os.path.join(root, d), sts.st_mode)
            for f in files:
                os.chmod(os.path.join(root, f), sts.st_mode)
    except PermissionError as e:
        logging.error(f"Error setting permissions on {project_root}: {e}")
        raise SystemExit(1)  # Indicate installation failure
    finally:  # default path with no exceptions - sts and permissions are set
        sys.path.extend([  # Add the project root to the system path
            os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')),
            os.path.join(os.path.dirname(os.path.realpath(__file__)), '.'),
            os.path.abspath(os.path.dirname(__file__))
        ])
    try:  
        log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        os.environ['LOG_DIR'] = log_dir
    except Exception as e:  
        logger.error(f"Error setting LOG_DIR: {e}", exc_info=True)
        raise SystemExit(1) 

    try:  
        log_file = os.path.join(log_dir, 'setup.log')
        os.environ['LOG_FILE'] = log_file
    except Exception as e:  
        logger.error(f"Error setting LOG_FILE: {e}", exc_info=True)
        raise SystemExit(1) 

    return project_root, log_dir, log_file, sts

def __starter():
    """Platform-agnostic .env initialization"""
    if os.name == 'nt':
        subprocess.run('copy /Y .env.example .env', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif os.name == 'posix' or os.name == 'mac': 
        subprocess.run('cp -f .env.example .env', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def __pipenv():
    """Wrapper for __starter(), handles potential errors"""
    try:
        __starter()
    except Exception as e:
        logger.error(f"Error installing dependencies: {e}", exc_info=True)
        raise SystemExit(1) 





if __name__ == "__main__":
    try:
        __pipenv()
        subprocess.run('pip install -r requirements.txt', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 

    except subprocess.CalledProcessError as e:
        logger.error(f"Error during setup: {e}")
        raise SystemExit(1)

    setup(
        name='ele',
        version='1.0',
        packages=find_packages(where='src', exclude=['opdb/*, logs/*, 2023dir/*, UFO/*, lit-llm/*']),
        install_requires=[
            'python-dotenv',
            'pathlib',
            'requests',
            'jupyter',
            'ipykernel',
            # ... other dependencies from your requirements.txt
        ],
        entry_points={
            'console_scripts': [
                'ele = ele.src.app:run',
            ]
        }
    )

else:  # if __name__ != "__main__": - failure-prone 'brittle' main for terminal invocation
    try:
        __starter()
    except Exception as e:
        if e.__traceback__:
            logger.error(f"Error initializing .env: {e}", exc_info=True)
            raise  # Re-raise the exception to halt execution
        else:
            logger.error(f"Error initializing .env: {e}")
            raise  # Re-raise the exception to halt execution
    finally:  # default path with no exceptions
        __mainpath()
        __pipenv()
        pass