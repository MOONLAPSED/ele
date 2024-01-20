#!/usr/bin/env python
#============ELEMENT.main.py_MIT_license_2024================#
# 1. imports + HOWTO: docstrings + Global logger = logger    #
# 2. Element + Attribute + Entity abstract classes           #
# 3. FileTypeSelector + FileHandlerInterface                 #
# 4. main() and if __name__ funcs                            #
##############################################################

from abc import ABC, abstractmethod
from datetime import datetime
from dataclasses import dataclass, field, validator
from dotenv import load_dotenv
from io import BytesIO
from pathlib import Path
from threading import Thread, Timer, Event, current_thread
from typing import Callable, Any, Optional, List, Dict, Tuple, Union, Set, Iterable, Iterator, TypeVar, Generic, Type, cast, overload

# HOWTO: docstrings
"""Short one line summary
(optional)Extended description of the class/function/method.

Args:
    arg1 (int): Description of arg1
    arg2 (str): Description of arg2
Returns:
    bool: Description of return value
(optional)Raises:"""
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  # Global logger



class Element(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def to_bytes(self) -> bytes:
        """Return the frame data as bytes with '---' and '\n' as delimiters, stripped of whitespace."""
        lines = self.to_str().splitlines()
        for line in lines:
            yield line.strip().encode('utf-8')
        yield b'---\n'

    @abstractmethod
    def to_str(self) -> str:
        """Return the frame data as a string representation with '---' and '\n' 'EOF' and '<im_end>' as delimiters."""
        pass

    def dict(self) -> dict:
        """Return a dictionary representation of the model."""
        return {
            "name": self.name,
            "description": self.description,
        }

@validator('name')
def validate_name(cls, name: Union[bytes, str]):
    if name is None:
        raise ValueError("Name must not be None")
    return bytes(name, 'utf-8')

@validator('description')
def validate_description(cls, description: Union[bytes, str]):
    if description is None:
        raise ValueError("Description must not be None")
    return bytes(description, 'utf-8')
    


class Attribute(Element):
    ALLOWED_TYPES = {"TEXT", "INTEGER", "REAL", "BLOB", "VARCHAR", "BOOLEAN", "UFS", "VECTOR", "TIMESTAMP", "EMBEDDING"}

    def __init__(self, name: str, description: str, data_type: str):
        super().__init__(name, description)
        if data_type not in self.ALLOWED_TYPES:
            raise ValueError(f"Invalid data type: {data_type}")
        self.data_type = data_type
    """Attribute inherits from Element and adds a data_type argument that must be one of the allowed types.
    
    Args:
        name (str): name of the attribute
        description (str): description of the attribute
        data_type (str): data type of the attribute
    Returns:
        None
    """

class Entity(Element):
    def __init__(self, name: str, description: str, elements: List[Element] = None):
        super().__init__(name, description)
        self.elements = elements if elements is not None else []
    """Entity inherits from Element, containing a list of Element instances.
    This allows Entity objects to contain Attribute objects and any other objects that are subclasses of Element.
    
    Args:
        name (str): name of the entity
        description (str): description of the entity
        elements (List[Element], optional): list of elements. Defaults to None.
    Returns:
        None
    """
class UnixFilesystem(Entity):
    def __init__(self, name: str, description: str, elements: List[Element], inode: int, pathname: str, filetype: str,
                 permissions: str, owner: str, group_id: int, PID: int, unit_file: str, unit_file_addr: str,
                 size: int, mtime: str, atime: str):
        super().__init__(name, description, elements)
        self.inode = inode
        self.pathname = pathname
        self.filetype = filetype
        self.permissions = permissions
        self.owner = owner
        self.group_id = group_id
        self.PID = PID
        self.unit_file = unit_file
        self.unit_file_addr = unit_file_addr
        self.size = size
        self.mtime = mtime
        self.atime = atime
    """UnixFilesystem is an example of Entity containing specific attributes that are relevant to a Unix filesystem.

    Args:
        Entity (Entity): Entity is the parent class of UnixFilesystem
    Returns:
        None
    """
    def __str__(self):
        return f"{self.inode}: {self.pathname}"

if __name__ == "__main__":
    load_dotenv()
    exit()
