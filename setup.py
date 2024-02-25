#!/usr/bin/env python
from pydantic import BaseModel, Field
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

class MySettings(BaseModel):
    required_date: date = Field(default_factory=datetime.now().date)
    required_int: int = Field(0, ge=0)  # Set default value here
    state: int = Field(0)  # New field to hold the state value

    def __init__(self):
        super().__init__()
        try:
            self.required_int = int(os.getenv("REQUIRED_INT", default=0))
            self.state = int(os.getenv("STATE", default=0))  # Load 'state' from .env file
        except ValueError as e:
            logging.basicConfig(filename='/logs/setup.log', level=logging.ERROR)
            logging.error(f"Error loading environment variables: {e}", exc_info=True)
            raise  # Re-raise the exception to halt execution
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
    settings = MySettings()
    settings.state = 1  # Set the state to 1 to indicate runtime pydantic validation has completed
    with open('.env', 'w') as env_file:  # Update state in .env file
        env_file.write(f"STATE={settings.state}\n")

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
    finally:
        settings.state = 0  # pydantic validation init and app has achieved runtime, set state to 0 (for possible re-initialization/debugging)
        with open('.env', 'w') as env_file:  # Update state in .env file
            env_file.write(f"STATE={settings.state}\n")
else:
    logging.basicConfig(filename='/logs/setup.log', level=logging.ERROR)
    logging.error("Setup error in setup.py", exc_info=True)