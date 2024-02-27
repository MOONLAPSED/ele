#!/usr/bin/env python

# setup.py-only functions, not for runtime or user-facing code
# 1. __log_error__
# 2. __shell_error__
# 3. __starter__
# 4 __pipenv__
# 5 __mainpath__
# 6 __entry_point__/pre-runtime-endpoint
# 7 BasedModel
# 8 main
# 9 validate_appsettings
# 10 __main__/runtime(init --> main.py)

from datetime import datetime, date
import logging
from setuptools import setup, find_packages
import subprocess
import os
import sys
from pydantic import BaseModel, Field, validator
from dataclasses import dataclass, field


def __log_error(message, log_file=os.path.join(os.path.dirname(__file__), 'logs', 'setup.log'), exc_info=False):
    """'Brittle' errors for system init only, not a user-facing error"""
    logging.basicConfig(filename=log_file, level=logging.ERROR)
    logging.error(message, exc_info=exc_info)
    return 1  # pre-custom logging

def __shell_error(command, exception, log_file=os.path.join(os.path.dirname(__file__), 'logs', 'setup.log')):
    """'Brittle' shell errors for system init only, not a user-facing error"""
    logging.basicConfig(filename=log_file, level=logging.ERROR)
    logging.error("Error executing command: %s", command, exc_info=exception)
    return 1  # pre-custom logging

def __starter():  # platform-agnostic .env init
    """'Brittle' starter for system init only, not a user-facing error"""
    if os.name == 'nt':  # Check if on Windows
        subprocess.run('copy /Y .env.example .env', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif subprocess.run('cp -f .env.example .env', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
        pass
    subprocess.run('pip install requirements.txt', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 

def __pipenv():  # wraper for __starter()
    try:
        __starter()    
    except Exception as e:
        if e.__traceback__:
            __log_error(f"Error installing pipenv: {e}", exc_info=True)
            raise  # Re-raise the exception to halt execution
        else:
            __log_error(f"Error installing pipenv: {e}")
            raise  # Re-raise the exception to halt execution
    return 0  # pre-custom logging


def __mainpath() -> tuple:
    project_root = os.path.abspath(os.path.dirname(__file__))  # Get project root

    try:
        sts=os.stat_result(os.stat(project_root))  # is there adequate permission to set permissions?
        # Set the children of the root directory to the same permissions as the root directory if so.
        for root, dirs, files in os.walk(project_root):
            for d in dirs:
                os.chmod(os.path.join(root, d), sts.st_mode)
            for f in files:
                os.chmod(os.path.join(root, f), sts.st_mode)
    except Exception as e:  # exit(1) if no os.stat object 'sts' is found
        if e.__traceback__:
            __log_error(f"Error setting permissions on {project_root}", exc_info=True)
            raise  # Re-raise the exception to halt execution
        else:
            __log_error(f"Error setting permissions on {project_root}")
            raise  # Re-raise the exception to halt execution

    finally:  # default path with no exceptions - sts and permissions are set
        sys.path.extend([  # Add the project root to the system path
            os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')),
            os.path.join(os.path.dirname(os.path.realpath(__file__)), '.'),
            os.path.abspath(os.path.dirname(__file__))
        ])
    try:
        log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        log_file = os.path.join(log_dir, 'setup.log')
        return project_root, log_file, log_dir, os.path.abspath(os.path.dirname(__file__))  # Return the project root, log file path, log directory path, and the absolute path of the current directory as a tuple

    except Exception as e:
        if e.__traceback__:
            __log_error(f"Error setting up main path: {e}", exc_info=True)
            raise  # Re-raise the exception to halt execution
        else:
            __log_error(f"Error setting up main path: {e}")
            raise  # Re-raise the exception to halt execution

    finally:  # default path with no exceptions
        sts_dict = vars(sts) if hasattr(sts, '__dict__') else {}
        sts_frozen = frozenset(sts_dict.items())  # freeze a dataclass of the sts object
        return project_root, log_dir, log_file, sts_frozen  


@dataclass
class SetupConfig:
    project_root: str
    log_dir: str
    log_file: str
    sts: frozenset  

def __entry_point():  # returns SetupConfig class object for BaseModel-use
    """ Data class which colates the results of the functions above """
    # logs, shell, stater and pip
    project_root, log_dir, log_file, sts = __mainpath()  # wraps __mainpath()
    @validator('project_root')
    def project_root_validator(v):
        if not os.path.exists(v):
            raise ValueError(f"Project root {v} does not exist")
        return v
    project_root: str = field(default_factory=__mainpath()[0])
    log_dir: str = field(default_factory=__mainpath()[1])
    log_file: str = field(default_factory=__mainpath()[2])
    sts: frozenset = field(default_factory=__mainpath()[3])
    return SetupConfig(project_root, log_dir, log_file, sts)


class BasedModel(BaseModel):
    required_date: date = Field(default_factory=datetime.now().date)
    required_int: int = Field(0, ge=0)  # Set default value here
    state: int = Field(0)  # New field to hold the state value
    def __init__(self):
        super().__init__()
        try:
            self.required_int = int(os.getenv("REQUIRED_INT", default=0))
            self.state = int(os.getenv("STATE", default=0))  # Load 'state' from .env file
            self.required_date = datetime.now().date()
        except Exception as e:
            if e.__traceback__:
                __log_error(f"Error initializing BasedModel: {e}", exc_info=True)
                raise  # Re-raise the exception to halt execution
            else:
                __log_error(f"Error initializing BasedModel: {e}")
                raise  # Re-raise the exception to halt execution
        finally:  # default path with no exceptions
            try:
                # Call other methods or classes to get the required values
                project_root, log_dir, log_file, sts = __mainpath()
                appsettings = BasedModel()
                appsettings.project_root = project_root
                appsettings.log_dir = log_dir
                appsettings.log_file = log_file
                appsettings.sts = sts
                
            except Exception as e:
                if e.__traceback__:
                    __log_error(f"Error initializing BasedModel: {e}", exc_info=True)
                    raise  # Re-raise the exception to halt execution
                else:
                    __log_error(f"Error initializing BasedModel: {e}")
                    raise  # Re-raise the exception to halt execution

def main():
    """Main function"""
    try:
        __pipenv()
    except Exception as e:
        if e.__traceback__:
            __log_error(f"Error running private method: {e}", exc_info=True)
            raise  # Re-raise the exception to halt execution
        else:
            __log_error(f"Error running private method: {e}")
            raise  # Re-raise the exception to halt execution
    finally:  # default path with no exceptions
        app = __entry_point()  # wrapper for __entrypoints
        return app


def validate_appsettings(appsettings):
    """Validate the appsettings"""
    try:
        project_root, log_file, log_dir, sts = appsettings

        if not os.path.exists(project_root):
            raise ValueError(f"Project root {project_root} does not exist")

        # Additional validation logic for other fields if needed

        return True  # Return True if all validations pass

    except Exception as e:
        __log_error(f"Error validating appsettings: {e}")
        return False  # Return False if any validation fails

def based_settings() -> tuple:
    appsettings = main()  # wrapper for app / main()
    if validate_appsettings(appsettings):  # wrapper for validate_appsettings()
        print("Appsettings are valid")
        based_model = BasedModel()
        based_model.project_root = appsettings.project_root
        based_model.log_dir = appsettings.log_dir
        based_model.log_file = appsettings.log_file
        based_model.sts = appsettings.sts
        return based_model, appsettings

def based_app():
    based_settings()
    based_app = based_settings()[0]
    if based_app.project_root == based_settings()[1].project_root:
        return based_app
    else:
        return 1

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
            'httpx'
        ],
        entry_points={
            'console_scripts': [
                'ele = ele.src.app:run',
            ]
        }
    )
    while based_app != 1:
        based_app()
    
    if based_app == 1:
        __log_error(f"Error running based_app: {based_app}")
        raise ValueError(f"Error running based_app: {based_app}")
    
else:  # if __name__ != "__main__": - failure-prone 'brittle' main for terminal invocation
    try:
        __starter()
    except Exception as e:
        if e.__traceback__:
            __log_error(f"Error installing dependencies: {e}", exc_info=True)
            raise  # Re-raise the exception to halt execution
        else:
            __log_error(f"Error installing dependencies: {e}")
            raise  # Re-raise the exception to halt execution
    finally:  # default path with no exceptions
        app = __entry_point()

# write a fucntion for cloning UFO and populating the *.lnk files/shortcuts