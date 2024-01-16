from datetime import datetime, date
from dotenv import load_dotenv
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pathlib
from pydantic import BaseModel, Field, validator, ConstrainedList as cl
import re
import requests
import select
import signal
import subprocess
import sys
import time
import typing
import typing_extensions

class MySettings(BaseSettings):
    """
    Configuration settings for the application.
    """
    launch_time: datetime = Field(default_factory=datetime.now)
    class Config:
        env_file = ".env"

    def setup_logger(self):
        logspath = Path("./logs")
        logspath.mkdir(parents=True, exist_ok=True)
        logfile = logspath / "logs.txt"

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

        file_handler = logging.FileHandler(str(logfile))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Preventing duplicate handlers
        if not logger.handlers:
            logger.addHandler(file_handler)

        logger.info(f"MySettings loaded with launch_type: {self.launch_type} and launch_directive: {self.launch_directive}.")

        return logger
        
class Element(BaseModel):
    name: str
    description: str

class Attribute(Element):
    name: str
    data_type: str

    @validator('data_type')
    def validate_data_type(cls, v):
        allowed_types = {"TEXT", "INTEGER", "REAL", "BLOB", "VARCHAR", "BYTES"}
        if v not in allowed_types:
            raise ValueError(f"Invalid data type: {v}")
        return v

class DataType(Attribute):
    def __repr__(self) -> str:
        return super().__repr__()
    pass

class TEXT(DataType):
    name: str

class INTEGER(DataType):
    name: str

class REAL(DataType):
    name: str

class BLOB(DataType):  # BLOBs are always a whole ele.sql table entry each 
    name: str

class VARCHAR(DataType):
    name: str
    length: int

class BYTES(DataType):  # ASCII BYTES objects
    name: str
    length: int

class Entity(BaseModel):
    name: str
    description: str
    attributes: list[Attribute] = []
    elements: list[Element] = []

class UnixFilesystem(BaseModel):
    inode: int
    pathname: str
    filetype: str
    permissions: str
    owner: str
    group_id: int
    PID: int
    unit_file: str
    unit_file_addr: str
    size: int
    mtime: datetime
    atime: datetime

    def __str__(self):
        return f"{self.inode}: {self.pathname}"

class MySettings(BaseModel):
    required_date: datetime

    class Config:
        env_file = ".env"

    def logger(self):
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
        self.logger = logging.getLogger(__name__)
        return self.logger

if __name__ == "__main__":
    load_dotenv()
    settings = MySettings()
    settings.logger()
