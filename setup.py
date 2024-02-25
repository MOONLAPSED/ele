#!/usr/bin/env python

from datetime import datetime, date
from time import sleep
import logging
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
from setuptools import setup, find_packages
import subprocess
import os
import sys
from dotenv import load_dotenv
from src.lager import Lager

def load_env_settings():
    try:
        load_dotenv()
    except ValueError:
        logging.basicConfig(filename='/logs/setup.log', level=logging.ERROR)
        logging.error("Error loading environment variables. Check your .env file.", exc_info=True)
        raise  # Re-raise the exception to halt execution

def copyenv():
    try:
        exe_command('cp .env.example .env')
        
    except ValueError:
        logging.basicConfig(filename='/logs/setup.log', level=logging.ERROR)
        logging.error("Error loading environment variables. Check your .env file.", exc_info=True)
        raise  # Re-raise the exception to halt execution

def entry_point():
    """This function is called by the setup.py file to set up the logger. It is not called by the main program."""
    try:
        copyenv()
        load_env_settings()
    except ValueError:
        logging.basicConfig(filename='/logs/setup.log', level=logging.ERROR)  # pre-custom logging
        logging.error("Error loading environment variables. Check your .env file.", exc_info=True)
        raise  # Re-raise the exception to halt execution
    lager = Lager()
    return lager

def exe_command(command, lager):
    try:
        lager.info(f'Executing command: {command}')
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        lager.debug(result.stdout.decode('utf-8'))
    except subprocess.CalledProcessError as exc:
        error_message = exc.stderr.decode('utf-8')
        lager.error(f'Command failed with error: {error_message}')
    except Exception as e:
        logging.basicConfig(filename='/logs/setup.log', level=logging.ERROR)  # pre-custom logging
        logging.error("Error executing command: {command}", exc_info=True)

def run_setup(install_commands, lager):
    try:
        for command in install_commands:
            exe_command(command)
        # ...
        exe_command('python main.py')  # runs main.py AFTER installing dependencies etc.
    except Exception as e:
        logging.basicConfig(filename='/logs/setup.log', level=logging.ERROR)
        logging.error(f"Error running setup: {e}", exc_info=True)


def mainpath():
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # is there adequate permission to expand the path?
    except Exception as e:
        print(e)
    finally:
        sys.path.extend([
            os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')),
            os.path.join(os.path.dirname(os.path.realpath(__file__)), '.'),
            os.path.abspath(os.path.dirname(__file__))
        ])
        # ... pre-git initialization
        return 0
def main():
    install_commands = [
        # 'conda install -c conda-forge jax xonsh',
        'start /wait /bin/OllamaSetup.exe',
        'pip install ollama',
        'pip install -r requirements.txt',
        # ...
    ]
    try:
        mainpath()
        run_setup(install_commands)
    except Exception as e:
        logging.basicConfig(filename='/logs/setup.log', level=logging.ERROR)
        logging.error(f"Error running setup or expanding path: {e}", exc_info=True)
        raise  # Re-raise the exception to halt execution

if __name__ == "__main__":
    setup(
        name='ele',
        version='1.0',
        packages=find_packages(where='src'),
        install_requires=[
            'python-dotenv',
            'pathlib',
            'requests',
            'jupyter',
            'ipykernel',
            'pandas',
            'matplotlib',
            'conda-forge::jax',
            'conda-forge::xonsh',
            'python-dotenv',
            'numpy',
            'httpx',
        ],
        entry_points={
            'console_scripts': [
                'ele = ele.src.app:run',
            ]
        }
    )

    try:
        entry_point()
    except Exception as e:
        logging.basicConfig(filename='/logs/setup.log', level=logging.ERROR)
        logging.error(f"Error running setup or expanding path: {e}", exc_info=True)
        raise  # Re-raise the exception to halt execution
else:
    logging.basicConfig(filename='/logs/setup.log', level=logging.ERROR)
    logging.error("Setup error in setup.py", exc_info=True)