#!/usr/bin/env python
# init cython, init dotenv, init matplotlib, numpy, transformers, pip, xonsh, jax, jupyter, ipykernel, and pytorch  
# cython: language_level=3
from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize

setup(
    name='ele',
    version='1.0',
    packages=find_packages(where='src'),
    ext_modules = cythonize("src/elements.pyx"),
    install_requires=[
        'Cython',
        'pydantic',
        'python-dotenv',
        'matplotlib',
        'numpy',
        'jax',
        'jupyter',
        'ipykernel',
    ],
    entry_points={
        'console_scripts': [
            'ele = ele:src.main',  
            'ele_source = ele:src.ele_source',
         ],
    },
)
