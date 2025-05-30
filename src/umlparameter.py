# Filename: umlparameter.py
# Authors: Steven Barnes
#          Evan Magill
#          John Hershey
#          Kyle Kalbach
#          Juliana Vinluan
#          Spencer Hoover
# Date: 2025-03-21
# Description: Parameter class definition.

from __future__ import annotations
from dataclasses import dataclass, field
import errors

@dataclass
class UmlParameter:
    """"""
    name:str
    umltype:str

    def rename_parameter(self,name:str) -> int: 
        """ Renames the parameter
        Params:   
                name: new name for the parameter
            Returns:
                0: if the parameter was successfully renamed
            Exceptions:
                InvalidNameError: if the name is invalid
        """
        errors.valid_name(name)
        self.name = name
        return 0
    
    def change_parameter_type(self, newtype:str) -> int:
        """ Changes the parameter type
        Params:   
                newtype: new type for the parameter
            Returns:
                0: if the parameter was successfully changed type
            Exceptions:
                InvalidTypeError: if the type does not conform with naming requirements
        """
        errors.valid_name(newtype) # type constrictions are the same as name constrictions
        self.umltype = newtype
        return 0

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'type': self.umltype
        }
    
    def __eq__(self, other:UmlParameter):
        """Dataclass hash not working apparently. Standard eq consistent with hash."""
        return self.name == other.name and self.umltype == other.umltype
    
    def __hash__(self):
        """Dataclass hash not working apparently. Standard hash."""
        return hash(self.name) + 3 * hash(self.umltype)