#!/usr/bin/env python
# init cython, init dotenv, init matplotlib, numpy, transformers, pip, xonsh, jax, jupyter, ipykernel, and pytorch 
# cython: language_level=3
from setuptools import setup, find_packages
from Cython.Build import cythonize

setup(
    name='ele',
    version='1.0',
    packages=find_packages('src'), 
    package_dir={'': 'src'},  # Specify the 'src' directory as the package directory
    ext_modules=cythonize('src/elements.pyx'),  # Compile the Cython code
    install_requires=[
        'Cython',
        'pydantic',
        'python-dotenv',
        'matplotlib',
        'numpy',
        'transformers',
        'pip',
        'xonsh',
        'jax',
        'jupyter',
        'ipykernel',
        'pytorch',
    ],
    entry_points={
        'console_scripts': [
            'ele = ele:main',  # add 'ele' to PATH
            'ele_source = ele:src.ele_source',
            'ele_main = ele:src.main',
        ],
    },
)