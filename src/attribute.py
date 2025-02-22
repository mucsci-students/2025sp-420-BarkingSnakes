# Filename: attribute.py
# Authors: John Hershey, Kyle kalbach
# Date 2-5/2025
# Description: class for object attribute methods and design

import logging
from dataclasses import dataclass
import errors

@dataclass
class Attribute:
    name:str

    def rename_attr(self,name:str) -> int:
        """Renames the Attribute
        Params: 
            name: new name for the Attribute
        Returns:
            0: if the Attribute was successfully renamed
            -1:if Attribute was not renamed
        Exceptions:
            UMLException if the new name is invalid or duplicate
        """""
        errors.valid_name(name)
        self.name = name
        return 0
    
    def to_dict(self) -> dict:
        return {
            'name': self.name
        }