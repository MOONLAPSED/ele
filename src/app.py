from pydantic import BaseModel, Field, validator
from dataclasses import dataclass, field
import os
import subprocess
from src.lager import Lager  # capital "L"
import sys
import uuid
from main import rt_main

app = rt_main()  # Use the pydantic app from setup.py






@dataclass
class SetupConfig:
    project_root: str = os.getenv('PROJECT_ROOT')
    log_dir: str = os.getenv('LOG_DIR')
    log_file: str = os.getenv('LOG_FILE')
    sts: os.stat_result = os.stat(os.getenv('PROJECT_ROOT'))
    sts_uid: int = field(init=False)
    hash_long: str = field(init=False)
    hash: str = field(init=False)

    def __post_init__(self):
        self.sts_uid = self.sts.st_uid

        try:
            self.hash_long = hash()
            self.hash = self.hash_long[:7]
        except:
            self.hash_long = None
            self.hash = None

        os.environ['HASH_LONG'] = self.hash_long
        os.environ['HASH'] = self.hash

        for e in str(self.sts_uid):
            os.environ[f'UID_{e}'] = str(self.sts_uid)



@app.on_event("startup")
def run():
    try:
        pass
    except:
        pass
    finally:
        pass

@app.on_event("shutdown")
def stop():
    try:
        pass
    except:
        pass
    finally:
        pass

if __name__ == "__main__":
    main_run()  # Call the run function from main.py
