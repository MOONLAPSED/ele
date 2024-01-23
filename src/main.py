#!/usr/bin/env python3
"""This module defines data models for handling frames, serializable objects, and entities."""
 #01 /src/main.py - what is this file and this module?                           #
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
import json
import logging
import os
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from dataclasses import dataclass, field, replace
from typing import List

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
        Delimiters are defined as '---' and '\n' or its analogues (EOF) or <|im_end|> or "..." etc for the start and end of a frame respectively.
        The frame model is a data structure that is independent of the source of the data.
        portability note: "delimiters" are established by the type of encoding and the arbitrary writing-style of the source data. eg: ASCII
    """
    @abstractmethod
    def to_bytes(self) -> bytes:
        """Return the frame data as bytes."""
        pass
    # TODO: class naive cython os.pipe() implementation to accept FrameModel as input and return bytes as output (inside the Ubuntu-22.04-LTS docker container)
    # TODO: from_bytes abstract?
 #03
class AbstractDataModel(FrameModel, ABC):
    """A data model is a data structure that contains the data of a frame aka a chunk of text contained by delimiters.
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
    """SerialObject is an abstract class that defines the interface for serializable objects within the abstract data model."""
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
    
    def to_bytes(self) -> bytes:
        """Return the frame data as bytes with '---' and '\n' as delimiters, stripped of whitespace."""
        lines = self.to_str().splitlines()
        
        # Join the lines using newline characters and encode the result to bytes
        contents = '\n'.join(line.strip() for line in lines)
        frame_data = f"---\n{contents}\n---\n".encode('utf-8')
        
        return frame_data

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
    _ALLOWED_TYPES = {"TEXT", "INTEGER", "REAL", "BLOB", "VARCHAR", "BOOLEAN", "UFS", "VECTOR", "TIMESTAMP", "EMBEDDING"}

    def __init__(self, name: str, description: str, data_type: str):
        super().__init__(name, description)
        if data_type not in self._ALLOWED_TYPES:
            raise ValueError(f"Invalid data type: {data_type}")
        self.data_type = data_type

    def to_str(self) -> str:
        """Return the string representation of the Attribute."""
        return f"Attribute: {self.name}, Type: {self.data_type}, Description: {self.description}"
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
@dataclass(frozen=True, slots=True)  # immutable + no __dict__ method
class SerializableEntity(Entity):
    serializer: ConcreteSerialModel

    def __init__(self, name: str, description: str, elements: List[Element] = None, serializer: ConcreteSerialModel = None):
        self.serializer = self.with_serializer(serializer)
        self.serializer.name = name
        super().__init__(name, description, elements)

    def with_serializer(self, serializer: ConcreteSerialModel):
        """
        Return a new instance of SerializableEntity with an updated serializer.
        Args:
            serializer (ConcreteSerialModel): The new serializer to use.
        Returns:
            SerializableEntity: A new instance with updated serializer.
        """
        return replace(self, serializer=serializer)


    def serialize(self) -> str:
        """Serialize the entity to a JSON string.

        Returns:
            str: JSON string representation of the entity.
        """
        return self.serializer.json()

 #10
class UnixFilesystem(Entity):
    def __init__(self, name: str, description: str, elements: List[Element] = None):
        super().__init__(name, description, elements)

    def to_str(self) -> str:
        """Return a string representation of the Element object."""
        return '\n<im_start>'.join([e.to_str() for e in self.elements]) + '\n<im_end>\n'

 #11
if __name__ == "__main__":
    def tests():
        # Create a new entity
        entity = Entity("Entity", "This is an entity")
        entity.elements.append(Attribute("Attribute", "This is an attribute", "INTEGER"))
        print(entity)
        print(entity.__dict__)
        for e in entity.elements:
            print(e.__dict__)
        # Create a new UFS entity
        ufx=UnixFilesystem("UnixFilesystem", "This is a unix filesystem")
        ufx.elements.append(Attribute("Attribute", "This is an attribute", "INTEGER"))
        ufx.elements.append(Attribute("Attribute2", "This is an attribute", "INTEGER"))
        entity.elements.append(ufx)
        print(ufx)
        print(ufx.__dict__)
        for u in ufx.elements:
            print(u.__dict__)

    try:
        tests()
    except Exception as e:
        print(e)
exit(1)