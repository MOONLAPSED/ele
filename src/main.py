from datetime import datetime, date
from dotenv import load_dotenv
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pathlib
from pydantic import BaseModel, Field, validator, ConstrainedList as CL
import re
import requests
import select
import signal
import subprocess
import sys
import time
import typing
import typing_extensions


# Define the abstract base class
class Entity:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name

class Element(Entity):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.dependencies = []
        self.children = []
        self.parent = None

# Define the concrete subclasses
class Attribute(Entity):
    def __init__(self, name, type):
        super().__init__(name, "Attribute of {}".format(name))
        self.type = type

    def __str__(self):
        return "{}: {}".format(self.name, self.type)

# Define the specific data types as subclasses of Attribute
class TEXT(Attribute):
    def __init__(self, name):
        super().__init__(name, "TEXT")

    def __str__(self):
        return "{}: TEXT".format(self.name)

class INTEGER(Attribute):
    def __init__(self, name):
        super().__init__(name, "INTEGER")

    def __str__(self):
        return "{}: INTEGER".format(self.name)

class REAL(Attribute):
    def __init__(self, name):
        super().__init__(name, "REAL")

    def __str__(self):
        return "{}: REAL".format(self.name)

class BLOB(Attribute):
    def __init__(self, name):
        super().__init__(name, "BLOB")

    def __str__(self):
        return "{}: BLOB".format(self.name)

class VARCHAR(Attribute):
    def __init__(self, name, length):
        super().__init__(name, "VARCHAR({})".format(length))
        self.length = length

    def __str__(self):
        return "{}: VARCHAR({})".format(self.name, self.length)

# Define UnixFilesystem as a subclass of Entity
class UnixFilesystem(Entity):
    def __init__(self, inode, pathname, filetype, permissions, owner, group_id, PID, unit_file, unit_file_addr, size, mtime, atime):
        super().__init__(inode, "Unix filesystem")
        self.pathname = pathname
        self.filetype = filetype
        self.permissions = permissions
        self.owner = owner
        self.group_id = group_id
        self.size = size
        self.PID = PID
        self.unit_file = unit_file
        self.unit_file_addr = unit_file_addr
        self.mtime = mtime
        self.atime = atime

    def __str__(self):
        return "{}: {}".format(self.inode, self.pathname)

# Define a Pydantic model for Obsidian-like folders
class ObsidianFolder(BaseModel):
    base_folder: str
    folders: CL[str]  # pydantic contained list

class mdjourney(BaseModel):
    """
    This class helps you select files of a specific type from a directory and its subdirectories.
    """

    def __init__(self, directory="..", file_extension="txt", logging_level=logging.INFO):
        """
        Args:
            directory: The directory to search for files. Defaults to the current directory.
            file_extension: The file extension to select. Defaults to "txt".
            logging_level: The logging level for the class. Defaults to logging.INFO.
        """
        self.directory = directory
        self.file_extension = file_extension
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging_level)

    def select_files(self):
        """
        This method selects files of the specified type and returns a dictionary containing their paths and contents.

        Returns:
            A dictionary where each key is a file path and each value is the contents of the corresponding file.
        """
        file_dict = {}
        for file_path in pathlib.Path(self.directory).glob(f"**/*.{self.file_extension}"):
            try:
                with open(file_path, "r") as file:
                    file_content = file.read()
                file_dict[str(file_path)] = file_content
                self.logger.info(f"Processed file: {file_path}")
            except IOError as e:
                self.logger.error(f"Error processing file: {file_path}", exc_info=True)

        if not file_dict:
            self.logger.info(f"No files found with extension '{self.file_extension}'")

        return file_dict

    def count_files(self):
        """
        Counts the total number of files in the specified directory and its subdirectories.

        Returns:
            Total number of files.
        """
        count = 0
        for _, _, files in os.walk(self):
            count += len(files)
        return count
    
    def get_file_stats(file_path):
        return {
            'size': os.path.getsize(file_path),
            'permissions': os.stat(file_path).st_mode,
            'uid': os.stat(file_path).st_uid,
            'gid': os.stat(file_path).st_gid,
            'atime': os.stat(file_path).st_atime,
            'mtime': os.stat(file_path).st_mtime,
            'ctime': os.stat(file_path).st_ctime,
        }
    
    def obsidian_folders(base_folder, folders):
        for folder in folders:
            folder_name = folder.replace(' ', '_')  # Replace spaces with underscores for file naming
            note_content = f"# {folder}"  # Markdown content for the folder note
            file_path = f"{base_folder}/{folder_name}.md"  # File path for the note
            
            with open(file_path, 'w') as file:
                file.write(note_content)
                print(f"Created folder: {folder}")
    
    def create_obsidian_folders(self, obsidian_folders: ObsidianFolder):
        """
        Creates Obsidian-like folders and subfolders based on the crawled data.
        """
        self.logger.info(f"Creating Obsidian-like folders and subfolders based on the crawled data...")
        start = time()

        for folder in obsidian_folders.folders:
            folder_path = os.path.join(obsidian_folders.base_folder, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

        end = time()
        self.logger.info(f"Created Obsidian-like folders and subfolders in {end - start} seconds.")



def main():
    fs = mdjourney(directory=".", file_extension="md")
    file_dict = fs.select_files()
    
    total_elapsed_time = 0  # Initialize total elapsed time variable
    total_files = mdjourney.count_files(fs.directory)
    start_time = time()
    max_processing_time = 5  # Set maximum allowed processing time per file
    
    for file_path, file_content in file_dict.items():
        print("#" * 50)
        print("File Path:   %s" % file_path)
        print("#" * 50)
        print("File Content:")
        
        try:
            content_start = file_content[:200]  # Get the first 200 characters of the content
            
            elapsed_time = time() - start_time
            if elapsed_time > max_processing_time:
                print(f"Timeout exceeded for file: {file_path}. Skipping...")
                continue
            
            total_elapsed_time += elapsed_time
            time_per_file = total_elapsed_time / total_files
            
            if time_per_file > max_processing_time:
                print("Processing time exceeded. Skipping remaining files.")
                break

            print("%s" % content_start)
            print(f"Elapsed time: {elapsed_time} seconds")
            print(f"Time per file: {time_per_file} seconds")

        except Exception as e:
            print(f"Error reading file: {file_path}")
            print(f"Error message: {str(e)}")
        
        print("@" * 50)
        print("File Path:   %s" % file_path)
        print("@" * 50)
    print("=" * 50)
    print(f"Total elapsed time: {total_elapsed_time} seconds")
    print(f"Average time per file: {total_elapsed_time / total_files} seconds")
    return file_dict

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
            print(f"Error loading environment variable: {e}")
    

if __name__ == "__main__":
    load_dotenv()  # Load environment variables

    settings = MySettings()
    settings.state = 1  # Set the state to 1
    
    # Update state in .env file
    with open('.env', 'w') as env_file:
        env_file.write(f"STATE={settings.state}\n")

    try:
        main()
    finally:
        # Update state to 0 after main() completes
        settings.state = 0
        # Update state in .env file
        with open('.env', 'w') as env_file:
            env_file.write(f"STATE={settings.state}\n")

