#!/usr/bin/env python

import logging
from logging.handlers import RotatingFileHandler
from setuptools import setup, find_packages
import subprocess
import os
from src.lager import *

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a file handler and set its level to DEBUG
    file_handler = RotatingFileHandler('setup.log', maxBytes=1024*1024, backupCount=5)
    file_handler.setLevel(logging.DEBUG)

    # Create a stream handler and set its level to INFO
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

def execute_command(command):
    try:
        logging.info(f'Executing command: {command}')
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.debug(result.stdout.decode('utf-8'))
    except subprocess.CalledProcessError as exc:
        error_message = exc.stderr.decode('utf-8')
        logging.error(f'Command failed with error: {error_message}')
    except Exception as e:
        error_message = str(e)
        logging.error(f'Unhandled exception: {error_message}')

def run_setup(install_commands):
    for command in install_commands:
        execute_command(command)

    execute_command('python main.py')


if __name__ == "__main__":
    setup_logger()

    install_commands = [
        # 'conda install -c conda-forge jax xonsh',
        'start /wait /bin/OllamaSetup.exe',
        'pip install ollama',
        'pip install -r requirements.txt',
        'cp .env.example .env',
        # ...
    ]

    run_setup(install_commands)

else:
    print("You have no src directory so please run /ele/setup.py directly")

setup(
    name='ele',
    version='1.0',
    packages=find_packages(where='src'),
    install_requires=[
        'conda-forge::jax',
        'conda-forge::xonsh',
        'python-dotenv',
        'matplotlib',
        'numpy',
        'pandas',
        'pathlib',
        'requests',
        'jupyter',
        'ipykernel',
        'httpx',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'ele = ele.src.lager:run', 
        ]
    }
)
