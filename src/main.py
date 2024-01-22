#!/usr/bin/env python3
 #01 /src/main.py - what is this file and this module?                            #
# +-----ele-------------Copyright-(c)-2024-MIT-license------moonlapsed----------+
# | 01) (this) glossary, imports, logs-init, and HOWTO docstring in this repo   |
# | 02) FrameModel abstract base class                                          |
# | 03) AbstractDataModel                                                       |
# | 04) SerialObject                                                            |
# | 05) ConcreteSerialModel                                                     |
# | 06) Element                                                                 |
# | 07) Attribute                                                               |
# | 07) Entity                                                                  |
# | 09) SerializableEntity                                                      |
# | 10) UnixFilesystem                                                          |
# | 11) if __name__==...                                                        |
# +=============================================================================+
 # Imports                                                                       #
import logging
import json
import sys
import uuid
import yaml
from abc import ABC, abstractmethod
from datetime import datetime
from dataclasses import dataclass, field
from typing import list

 # HOWTO: docstrings
"""Short one line summary
(optional)Extended description of the class/function/method.

Args:
    arg1 (int): Description of arg1
    arg2 (str): Description of arg2
Returns:
    bool: Description of return value
(optional)Raises:"""

 # Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  # Global logger

 #02
class FrameModel(ABC):
    """A frame model is a data structure that contains the data of a frame aka a chunk of text contained by dilimiters.
        Delimiters are defined as '---' and '\n' or its analogues (EOF) or <|in_end|> or "..." etc for the start and end of a frame respectively.)
        the frame model is a data structure that is independent of the source of the data.
        portability note: "dilimiters" are established by the type of encoding and the arbitrary writing-style of the source data. eg: ASCII
    """
    @abstractmethod
    def to_bytes(self) -> bytes:
        """Return the frame data as bytes."""
        pass
    # TODO: class naive cython os.pipe() implementation to accept FrameModel as input and return bytes as output (inside the Ubuntu-22.04-LTS docker container)
    # TODO: from_bytes abstract?
 #03
class AbstractDataModel(FrameModel, ABC):
    """A data model is a data structure that contains the data of a frame aka a chunk of text contained by dilimiters.
        It has abstract methods --> to str and --> to os.pipe() which are implemented by the concrete classes.
    """
    @abstractmethod
    def to_pipe(self, pipe) -> None:
        """Write the model to a named pipe."""
        pass

    @abstractmethod
    def to_str(self) -> str:
        """Return the frame data as a string representation."""
        pass
    # TODO: frozen @dataclass decorator to ensure that the class is immutable + fast
 #04
class SerialObject(AbstractDataModel, ABC):
    """SerialObject is an abstract class that defines the interface for serializable objects within the abstract data model.
        Inputs:
            AbstractDataModel: The base class for the SerialObject class

        Returns:
            SerialObject object
    
    """
    @abstractmethod
    def dict(self) -> dict:
        """Return a dictionary representation of the model."""
        pass

    @abstractmethod
    def json(self) -> str:
        """Return a JSON string representation of the model."""
        pass

 #05
@dataclass
class ConcreteSerialModel(SerialObject):
    """
    This concrete implementation of SerialObject ensures that instances can
    be used wherever a FrameModel, AbstractDataModel, or SerialObject is required,
    hence demonstrating polymorphism.
        Inputs:
            SerialObject: The base class for the ConcreteSerialModel class

        Returns:
            ConcreteSerialModel object        
    """

    name: str
    age: int
    timestamp: datetime = field(default_factory=datetime.now)

    def to_bytes(self) -> bytes:
        """Return the JSON representation as bytes."""
        return self.json().encode()

    def to_pipe(self, pipe) -> None:
        """
        Write the JSON representation of the model to a named pipe.
        TODO: actual implementation needed for communicating with the pipe.
        """
        pass

    def to_str(self) -> str:
        """Return the JSON representation as a string."""
        return self.json()

    def dict(self) -> dict:
        """Return a dictionary representation of the model."""
        return {
            "name": self.name,
            "age": self.age,
            "timestamp": self.timestamp.isoformat(),
        }

    def json(self) -> str:
        """Return a JSON representation of the model as a string."""
        return json.dumps(self.dict())
 #06
class Element(ABC):
    """
    Composable-serializers, abstract interfaces, and polymorphism are used to create a "has-a" relationship between the serializer and the entity.
    """
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
 #07
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
 #08
class Entity(Element):
    def __init__(self, name: str, description: str, elements: list[Element] = None):
        super().__init__(name, description)
        self.elements = elements if elements is not None else []
        self.uuid = uuid.uuid4()
    """Entity inherits from Element, containing a list of Element instances.
    This allows Entity objects to contain Attribute objects and any other objects that are subclasses of Element.
    
    Args:
        name (str): name of the entity
        description (str): description of the entity
        elements (List[Element], optional): list of elements. Defaults to None.
    Returns:
        None
    """

    def __str__(self) -> str:
        """Return a user-friendly string representation of the Element object."""
        return f"Name: {self.name}\nDescription: {self.description}"

    def to_str(self) -> str:
        """Return a string representation of the Element object."""
        return '\n<im_start>'.join([e.to_str() for e in self.elements]) + '\n<im_end>\n'
 #09
@dataclass(frozen=True, slots=True)  # immutable/frozen by default + no __dict__ method
class SerializableEntity(Entity):
    """Entity composed with a serial model
    example:
        e = SerializableEntity("name", "desc") 
        e.serializer = ConcreteSerialModel("name", 0, None)  
        print(e.serialize())"""
    serializer: ConcreteSerialModel = None
    
    def serialize(self):
        if self.serializer:
            return self.serializer.to_json()
        else:
            return json.dumps(self.dict())

 #10
class UnixFilesystem(SerializableEntity):
    def __init__(self, name: str, description: str, elements: list[Element], inode: int, pathname: str, filetype: str,
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
    
    def __str__(self):
        return f"{self.inode}: {self.pathname}"

    def to_str(self) -> str:
        """Return a string representation of the UnixFilesystem object."""
        return f"""\
name: {self.name}
description: {self.description}
inode: {self.inode}
pathname: {self.pathname}
filetype: {self.filetype}
permissions: {self.permissions}
owner: {self.owner}
group_id: {self.group_id}
PID: {self.PID}
unit_file: {self.unit_file}
unit_file_addr: {self.unit_file_addr}
size: {self.size}
mtime: {self.mtime}
atime: {self.atime}
"""


class VirtualFolder(Entity):
    def __init__(self, name: str, description: str, elements: list[Element], path: str):
        super().__init__(name, description, elements)
        self.path = path
    
    def __str__(self):
        return f"{self.path}"


def create_virtual_file(path, content):
    with open(path, "w") as f:
        f.write("---\n")
        if isinstance(content, dict):
            f.write(yaml.dump({"content": content}))
        else:
            f.write(content)
        f.write("---\n")

 #11
if __name__ == "__main__":
    """
    Displays the output of the different methods of the model using an example UnixFilesystem object, often called just 'ufs'.
    """
    create_virtual_file("virtual_folder/my_file.md", "This is the file content.")
    create_virtual_file("virtual_folder/my_file.json", json.dumps({"name": "my_file", "uuid": '0XF200000000000000'}))
    
    ufs = UnixFilesystem("my_file", "my_file", [], 1, "virtual_folder/my_file.md", "file", "rw-r--r--", "root", 0, 0, "", "", 10, "1619166557", "1619166557")
    print(ufs)
    print(ufs.serialize())
    print(ufs.to_str())
    print(list(ufs.to_bytes()))
    print(ufs.dict())
    print(ufs.json())
    ufs.to_pipe(sys.stdout)
    ufs.to_pipe(sys.stdout, "json")
    ufs.to_pipe(sys.stdout, "yaml")