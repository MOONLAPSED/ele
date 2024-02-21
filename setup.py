#!/usr/bin/env python

from setuptools import setup, find_packages
import subprocess

def execute_command(command):  # not for use at or after runtime
    try:
        print(f'Executing command: {command}')
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode('utf-8'))
    except subprocess.CalledProcessError as exc:
        print(f'Command failed with error: {exc.stderr.decode("utf-8")}')
    except Exception as e:
        print(f'Unhandled exception: {e}')

def run_setup(install_commands):
    for command in install_commands:
        execute_command(command)

    execute_command('python main.py')

if __name__ == "__main__":
    install_commands = [
        'conda install -c conda-forge jax xonsh',
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
})