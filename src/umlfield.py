# Filename: field.py
# Authors: Kyle Kalbach, Steven Barnes, Evan Magill, Juliana , Spencer
# Date: 2025-02-24
# Description: Field class and methods

from dataclasses import dataclass
import errors
from enum import Enum

class FieldType(Enum):
    STRING = 0
    INTEGER = 1
    FLOAT = 2
    COMPLEX = 3
    LIST = 4
    TUPLE = 5
    RANGE = 6
    DICT = 7
    SET = 8
    FROZENSET = 9
    BOOLEAN = 10
    NONE = 11
    OTHER = 12


@dataclass
class UmlField:
    name:str
    type:FieldType

    def rename_field(self,name:str) -> int:
         """ Renames the Field
        Params:   
            name: new name for the field
        Returns:
            0: if the Field was successfully renamed
        Exceptions:
            InvalidNameError: if the name is invalid
        """
         errors.valid_name(name)
         self.name = name
         return 0
    
    def to_dict(self) -> dict:
        return {
            'name': self.name
        }
    
    def __eq__(self, other):
        """
        Checks equality between UmlFields.
        """
        if self.type == other.type:
            return True
        return False
    
    def __hash__(self):
        """
        Produces a hashed value such that UmlFields considered equal by __eq__ will produce the same hash value.
        """
        return hash((id(self.name)) * 3 + self.type * 5)
    