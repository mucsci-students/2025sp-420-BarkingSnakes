# Filename: umlmethod.py
# Authors: Steven Barnes
#          Evan Magill
#          John Hershey
#          Kyle Kalbach
#          Juliana Vinluan
#          Spencer Hoover
# Date: 2025-02-25
# Description: Encapsulation of a method on a UML Class.

from __future__ import annotations

from dataclasses import dataclass, field

from umlparameter import UmlParameter

import errors


@dataclass
class UmlMethod:
    """"""
    name:str
    params:dict[str, UmlParameter] = field(default_factory= lambda: dict())
    
    @property
    def arity(self) -> int:
        """The number of parameters a method has."""
        return len(self.params)

    def add_parameter(self, parameter:str) -> int:
        """Adds an UmlParameter the UmlMethod.
        Params:
            name: name of the parameter to add
        Returns:
            0 if the parameter was successfully added  
            a number corresponding to an error in the errors class
            if a parameter was not removed fromm the class
        Exceptions:
            InvalidNameError
            DuplicateParameterError
        """
        errors.valid_name(parameter)

        if parameter in self.params:
            raise errors.DuplicateParameterException()
        self.params[parameter] = UmlParameter(parameter)
        return 0
    
    def add_parameters(self, parameters:list[str]) -> int:
        """Adds an UmlParameter the UmlMethod.
        Params:
            name: name of the parameter to add
        Returns:
            0 if the parameter was successfully added  
            a number corresponding to an error in the errors class
            if a parameter was not removed form the class
        Exceptions:

        """
        for param in parameters:
            self.add_parameter(param)
        return 0

    def remove_parameter(self, parameter:str) -> int:
        """Removes an UmlParameter from the UmlMethod.
        Params:
            name: name of the parameter to remove
        Returns:
            0 if the parameter was successfully removed  
            a number corresponding to an error in the errors class
            if a parameter was not removed form the class
        Exceptions:
            NoSuchParameterException
        """
        if parameter not in self.params:
            raise errors.NoSuchParameterExcept()
        self.params.pop(parameter)

        return 0
    
    def rename_parameter(self, parameter:str, newname:str) -> int:
        """Renames an UmlParameter from the UmlMethod.
        Params:
            name: name of the parameter to rename
            new: the new name of the parameter
        Returns:
            0 if the parameter was successfully renamed  
            a number corresponding to an error in the errors class
            if a parameter was not removed form the class
        Exceptions:
            InvalidNameError
            NoSuchParameterException
        """
        if parameter not in self.params:
            raise errors.NoSuchParameterException()
        errors.valid_name(newname)

        self.params.pop(parameter)
        self.add_parameter(newname)
        return 0
    
    def clear_parameters(self):
        """Removes all UmlParameter from the UmlMethod.
        Params:

        Returns:
            0 if the parameter was successfully added  
            a number corresponding to an error in the errors class
            if a parameter was not removed form the class
        Exceptions:
            
        """
        self.params.clear()

    def replace_parameters(self, parameters:list[str]):
        """Replaces all UmlParameter from the UmlMethod.
        Params:
            parameters: a list of parameter names to replace existing parameters with.
        Returns:
            0 if the parameter was successfully added  
            a number corresponding to an error in the errors class
            if a parameter was not removed form the class
        Exceptions:
            
        """

        self.clear_parameters()
        self.add_parameters(parameters)

    def to_dict(self):
        return {
            'name': self.name,
            'params': [p.to_dict() for p in self.params.values()]
        }
    
    def __eq__(self, other:UmlMethod):
        return self.name == other.name and self.arity == other.arity
