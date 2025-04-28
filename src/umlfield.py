# Filename: field.py
# Authors: Kyle Kalbach, Steven Barnes, Evan Magill, Juliana Vinluan , Spencer Hoover
# Date: 2025-02-24
# Description: Field class and methods

from dataclasses import dataclass
import errors

@dataclass
class UmlField:
    name:str
    type:str

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
     
    def change_type(self,type:str):
        """changes the field's type
        Params:   
            type: the type of the field
        Returns:
            None
        Exceptions:
            InvalidNameError: if the type is invalid
        """
        errors.valid_name(type)
        self.type = type
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'type': self.type
        }
