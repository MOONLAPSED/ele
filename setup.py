import subprocess
import os
import sys
import logging
from setuptools import setup
import logging.config

try:  # Configure setup logging
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file_handler': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.abspath(os.path.join(os.path.dirname(__file__), 'logs', 'setup.log')),
                'maxBytes': 10 * 1024 * 1024,  # 10MB
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
    # Basic logging setup for setup.py in case of configuration error
    log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'logs', 'setup.log'))
    logging.basicConfig(filename=log_file_path, level=logging.INFO)
    logging.error(f"Error setting up logging configuration: {e}")
    raise SystemExit(1)  # Indicate installation failure (no logging)
finally:
    logging.info("Setup-logging initiated.")


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
    finally:
        sys.path.extend([
            os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')),
            os.path.join(os.path.dirname(os.path.realpath(__file__)), '.'),
            os.path.abspath(os.path.dirname(__file__))
        ])

    try:
        log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        os.environ['LOG_DIR'] = log_dir
    except Exception as e:
        logging.error(f"Error setting LOG_DIR: {e}", exc_info=True)
        raise SystemExit(1)

    try:
        log_file = os.path.join(log_dir, 'setup.log')
        os.environ['LOG_FILE'] = log_file
    except Exception as e:
        logging.error(f"Error setting LOG_FILE: {e}", exc_info=True)
        raise SystemExit(1)

    return project_root, log_dir, log_file, sts

def __starter():
    """Platform-agnostic .env initialization"""  # agnostic but only works on windows, lol
    if os.name == 'nt':
        subprocess.run('copy /Y .env.example .env', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run('pip install -r requirements.txt', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
def __pipenv() -> tuple:
    """Wrapper for __starter(), handles potential errors"""
    try:
        __starter()
        mp = __mainpath()
        return mp
    except Exception as e:
        logging.error(f"Error installing dependencies: {e}", exc_info=True)
        raise SystemExit(1)

if __name__ == "__main__":
    try:
        mp = __pipenv()
        logging.info("Dependencies installed.\n|main_path:|\n{mp}")
        # caddy/GO initialization & ipykernel initialization & jupyter notebook+server initialization
        # subprocess.run('python -m jupyter -dir .', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during setup: {e}")
        raise SystemExit(1)

def read_requirements():
    with open('requirements.txt') as req:
        requirements = req.read().splitlines()
    return requirements

setup(
    name='ele',
    version='1.0',
    install_requires=read_requirements(),
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'ele = ele.src.app:run',
        ]
    }
)
