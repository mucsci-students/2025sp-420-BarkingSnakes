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
    params:list[UmlParameter]
    return_type:str
    
    #@property
    #def arity(self) -> int:
    #    """The number of parameters a method has."""
    #    return len(self.params)
    
    @property
    def overloadID(self) -> str:
        """Produces a string to be used to distinguish overloads.
        Returns:
            The string of all the types of parameters in the parameter list
            in order, space separated.
        """
        return " ".join([param.umltype for param in self.params])

    def add_parameter(self, parameter_name:str, parameter_type:str) -> int:
        """Adds an UmlParameter the UmlMethod.
        Params:
            name: name of the parameter to add
        Returns:
            0 if the parameter was successfully added  
            a number corresponding to an error in the errors class
            if a parameter was not added to the class
        Exceptions:
            InvalidNameError
            DuplicateParameterError
        """
        errors.valid_name(parameter_name)
        errors.valid_name(parameter_type)

        if parameter_name in [param.name for param in self.params]:
            raise errors.DuplicateParameterException()
        self.params.append(UmlParameter(parameter_name, parameter_type))
        return 0
    
    def add_parameters(self, parameters:list[tuple[str, str]]) -> int:
        """Adds an UmlParameter the UmlMethod.
        Params:
            name: name of the parameter to add
        Returns:
            0 if the parameter was successfully added  
            a number corresponding to an error in the errors class
            if a parameter from the list was not added
        Exceptions:
            InvalidNameError
            DuplicateParameterError
        """
        for (parameter_name, parameter_type) in parameters:
            self.add_parameter(parameter_name, parameter_type)
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
        #TODO refactor
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
        #TODO refactor
        if parameter not in self.params:
            raise errors.NoSuchParameterExcept()
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

    def replace_parameters(self, parameters:list[tuple[str, str]]):
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
        #TODO refactor
        return {
            'name': self.name,
            'params': [p.to_dict() for p in self.params.values()]
        }
    
    def __eq__(self, other:UmlMethod):
        return self.name == other.name and self.arity == other.arity
