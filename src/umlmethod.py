# Filename: umlmethod.py
# Authors: Steven Barnes
#          Evan Magill
#          John Hershey
#          Kyle Kalbach
#          Juliana Vinluan
#          Spencer Hoover
# Creation Date: 2025-03-23, Last Edit Date: 2025-05-12
# Description: Encapsulation of a method on a UML Class.

from __future__ import annotations

from dataclasses import dataclass, field

from umlparameter import UmlParameter

import errors


@dataclass
class UmlMethod:
    """"""
    name:str
    return_type:str
    params:list[UmlParameter]
    
    @property
    def overloadID(self) -> str:
        """Produces a string to be used to distinguish overloads.
        Returns:
            The string of all the types of parameters in the parameter list
            in order, space separated.
        """
        return " ".join([param.umltype for param in self.params])
    
    def change_type(self, new_type:str):
        """Changes the type of the method
        Params:
            new_type: the new type of the method
        Returns:
            None
        Exceptions:
            InvalidNameError
        """
        errors.valid_name(new_type)
        self.return_type = new_type

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
            parameters: a list of tuples of the form (parameter_name:str, parameter_type:str)
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

    def remove_parameter(self, parameter_name:str) -> int:
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
        for i in range(len(self.params)):
            if self.params[i].name == parameter_name:
                self.params.pop(i)
                return 0
        raise errors.NoSuchParameterException()
            
    def rename_parameter(self, oldname:str, newname:str) -> int:
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
        errors.valid_name(newname)

        if newname in [param.name for param in self.params]:
            raise errors.DuplicateParameterException()

        for i in range(len(self.params)):
            if self.params[i].name == oldname:
                self.params[i].name = newname
                return 0
        raise errors.NoSuchParameterException()
    
    def replace_parameter(self, oldname:str, newname:str, newtype:str):
        """Replace the parameter with the name oldname, with a new parameter with name newname and type newtype"""
        errors.valid_name(newname)
        errors.valid_name(newtype)

        if newname != oldname and newname in [param.name for param in self.params]:
            # the newname is allowed to be the same as the oldname.
            # The newname must not exist anywhere else in the parameter list.
            raise errors.DuplicateParameterException()
        for i in range(len(self.params)):
            if self.params[i].name == oldname:
                self.params[i].name = newname
                self.params[i].umltype = newtype
                return 0
        raise errors.NoSuchParameterException()

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

    def replace_all_parameters(self, parameters:list[tuple[str, str]]):
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
            'return_type': self.return_type,
            'params': [p.to_dict() for p in self.params]
        }
    


    def __eq__(self, other:UmlMethod):
        """dataclass default __eq__ is unsuitable due to non-comparable list params.
        """
        if self.name != other.name or self.return_type != other.return_type or len(self.params) != len(other.params):
            return False
        for i in range(len(self.params)):
            if self.params[i] != other.params[i]:
                return False
        return True
    
