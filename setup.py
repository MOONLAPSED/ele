#!/usr/bin/env python

from datetime import datetime, date
import logging
from setuptools import setup, find_packages
import subprocess
import os
import sys
from dotenv import load_dotenv
from src.lager import Lager
from pydantic import BaseModel, Field
from datetime import datetime, date


def load_env_settings():
    try:
        load_dotenv()
    except ValueError:
        log_file = os.path.join(os.path.dirname(__file__), 'logs', 'setup.log')
        logging.basicConfig(filename=log_file, level=logging.ERROR)  # pre-custom logging
        logging.error("Error loading environment variables. Check your .env file.", exc_info=True)
        raise  # Re-raise the exception to halt execution


def copyenv():
    try:
        exe_command('cp .env.example .env')

    except ValueError:
        log_file = os.path.join(os.path.dirname(__file__), 'logs', 'setup.log')
        logging.basicConfig(filename=log_file, level=logging.ERROR)  # pre-custom logging
        logging.error("Error loading environment variables. Check your .env file.", exc_info=True)
        raise  # Re-raise the exception to halt execution


def entry_point():
    """This function is called by the setup.py file to set up the logger. It is not called by the main program."""
    try:
        copyenv()
        load_env_settings()
    except ValueError:
        log_file = os.path.join(os.path.dirname(__file__), 'logs', 'setup.log')
        logging.basicConfig(filename=log_file, level=logging.ERROR)  # pre-custom logging
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
    except Exception:
        log_file = os.path.join(os.path.dirname(__file__), 'logs', 'setup.log')
        logging.basicConfig(filename=log_file, level=logging.ERROR)  # pre-custom logging
        logging.error("Error executing command: {command}", exc_info=True)


def run_setup(install_commands):
    try:
        lager = Lager()
        for command in install_commands:
            exe_command(command)
        # ...
        exe_command('python main.py')  # runs main.py AFTER installing dependencies etc.
    except Exception as e:
        log_file = os.path.join(os.path.dirname(__file__), 'logs', 'setup.log')
        logging.basicConfig(filename=log_file, level=logging.ERROR)  # pre-custom logging
        logging.error(f"Error running setup: {e}", exc_info=True)


class MySettings(BaseModel):
    required_date: date = Field(default_factory=datetime.now().date)
    required_int: int = Field(0, ge=0)  # Set default value here
    state: int = Field(0)  # New field to hold the state value

    def __init__(self):
        super().__init__()
        try:
            self.required_int = int(os.getenv("REQUIRED_INT", default=0))
            self.state = int(os.getenv("STATE", default=0))  # Load 'state' from .env file
            sys.path.extend([
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
                os.path.join(os.path.dirname(os.path.realpath(__file__)), '.'), 
            ])
        except Exception as e:
            log_file = os.path.join(os.path.dirname(__file__), 'logs', 'setup.log')
            logging.basicConfig(filename=log_file, level=logging.ERROR)  # pre-custom logging
            logging.error(f"Error loading environment variables: {e}", exc_info=True)
            raise  # Re-raise the exception to halt execution


def mainpath(log_file):
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
        subprocess.run('pip install -r requirements.txt', shell=True)
        log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'setup.log')


def main(log_file):
    install_commands = [
        # 'conda install -c conda-forge jax xonsh',
        # 'pip install -r requirements.txt',
        'start /wait /bin/OllamaSetup.exe',
        'pip install ollama',
        # ...
    ]
    
    try:
        mainpath(log_file)
        run_setup(install_commands)
    except Exception as e:
        logging.basicConfig(filename=log_file, level=logging.ERROR)  # pre-custom logging
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
    main()

    try:
        entry_point()

    except Exception as e:
        log_file = os.path.join(os.path.dirname(__file__), 'logs', 'setup.log')
        logging.basicConfig(filename=log_file, level=logging.ERROR)  # pre-custom logging
        logging.error(f"Error running setup or expanding path: {e}", exc_info=True)
        raise  # Re-raise the exception to halt execution
else:
    log_file = os.path.join(os.path.dirname(__file__), 'logs', 'setup.log')
    logging.basicConfig(filename=log_file, level=logging.ERROR)  # pre-custom logging
    logging.error("Setup error in setup.py", exc_info=True)