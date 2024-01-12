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


class Element(BaseModel):
    name: str
    description: str

class Attribute(Element):
    name: str
    data_type: str

    @validator('data_type')
    def validate_data_type(cls, v):
        allowed_types = {"TEXT", "INTEGER", "REAL", "BLOB", "VARCHAR"}
        if v not in allowed_types:
            raise ValueError(f"Invalid data type: {v}")
        return v

class DataType(Attribute):
    pass

class TEXT(DataType):
    name: str

class INTEGER(DataType):
    name: str

class REAL(DataType):
    name: str

class BLOB(DataType):
    name: str

class VARCHAR(DataType):
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
    load_dotenv()  # Move this line here to ensure environment variables are loaded before creating MySettings instance
    settings = MySettings()
    settings.logger()