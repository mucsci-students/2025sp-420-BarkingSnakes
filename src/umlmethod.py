# Filename: umlmethod.py
# Authors: Steven Barnes
#          Evan Magill
#          John Hershey
#          Kyle Kalbach
#          Juliana Vinluan
#          Spencer Hoover
# Date: 2025-03-23
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
    
# deprecated to enforce use of _overload_exists
#
#    def __eq__(self, other:UmlMethod):
#        """Proxy for overload collision. 
#            If two methods are not allowed to simultaneously exist (same name and parameter types with same order), returns True.
#        """
#        return self.name == other.name and self.overloadID == other.overloadID
#    
#    def __hash__(self):
#        """Hash consistent with __eq__ as a proxy for overload collision.
#        """
#        return hash(self.name) + 3 * hash(self.overloadID)
