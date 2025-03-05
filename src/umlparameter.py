# Filename: umlparameter.py
# Authors: Steven Barnes
#          Evan Magill
#          John Hershey
#          Kyle Kalbach
#          Juliana Vinluan
#          Spencer Hoover
# Date: 2025-02-27
# Description: Parameter class definition.

from dataclasses import dataclass, field
import errors

@dataclass
class UmlParameter:
    """"""
    name:str

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

    def to_dict(self) -> dict:
        return {
            'name': self.name
        }