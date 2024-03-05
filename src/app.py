from pydantic import BaseModel, Field, validator
from dataclasses import dataclass, field
from datetime import datetime, date
from dotenv import load_dotenv
import os
import subprocess
from src.lager import Lager  # capital "L"
import sys
from tablib import Dataset
import uuid
from main import main as ml_main

ml = ml_main()
ml.info("instantiated from main")
load_dotenv()

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
            self.hash_long = os.environ['HASH_LONG']
            self.hash = os.environ['HASH']
        except:
            self.hash_long = None
            self.hash = None

        os.environ['HASH_LONG'] = self.hash_long
        os.environ['HASH'] = self.hash

        for e in str(self.sts_uid):
            print(f"{e.encode()} {os.environ[f'UID_{e}']} = {str(self.sts_uid)}")


class BasedModel(BaseModel):
    required_date: date = Field(default_factory=datetime.now().date)

    def __init__(self):
        super().__init__()
        try:
            self.state = int(os.getenv("STATE", default=0))  # Load 'state' from .env file
            if os.environ['HASH_LONG'] is not None or -1: self.state += 1
            SetupConfig()
            ml.info(f"BasedModel initialized with state {self.state}")
        except Exception as e:
            if e.__traceback__:
                ml.error(f"Error initializing BasedModel: {e}", exc_info=True)
                raise  # Re-raise the exception to halt execution
            else:
                ml.error(f"Error initializing BasedModel: {e}")
                raise  # Re-raise the exception to halt execution
        finally:
            # pretty print with tablib tabular-style
            print(tablib.Dataset(data=self.dict(exclude={'state'}).values()).export('html'))

        self.state = 0  # Reset state to 0
        self.git_tags = subprocess.check_output(['git', 'tag', '--list']).decode().split('\n')
        self.git_tags = [t for t in self.git_tags if t != '']  # Remove empty strings
        self.git_tag_latest = self.git_tags[-1]  # Get the latest tag
        # self.git_tag_latest_short = self.git_tag_latest.split('-')[0]  # Get the short version of the latest tag
#@app.on_event("startup")
def run():
    try:
        pass
    except:
        pass
    finally:
        pass

#@app.on_event("shutdown")
def stop():
    try:
        pass
    except:
        pass
    finally:
        pass

def main():
    pass

if __name__ == "__main__":
    main()