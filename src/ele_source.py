#!/usr/bin/env python
# init and re-init module and source all the files in the src folder
import subprocess

def rollout():
    subprocess.call(["./src/ele_source.sh"])