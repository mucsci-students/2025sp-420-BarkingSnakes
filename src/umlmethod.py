# Filename: umlmethod.py
# Authors: Steven Barnes
#          Evan Magill
#          John Hershey
#          Kyle Kalbach
#          Juliana Vinluan
#          Spencer Hoover
# Date: 2025-02-25
# Description: Encapsulation of a method on a UML Class.

class UmlParameter:
    """"""

class UmlMethod:
    """"""

    def __init__(self, name:str, params:dict[str, UmlParameter]):
        """"""
        self.name = name
        self.params:dict[str, UmlParameter] = params
    
    @property
    def arity(self) -> int:
        """The number of parameters a method has."""
        return len(self.params)

    def add_parameter(self, parameter:str):
        """Adds an UmlParameter the UmlMethod.
        Params:
            name: name of the parameter to add
        Returns:
            0 if the parameter was successfully added  
            a number corresponding to an error in the errors class
            if a parameter was not removed form the class
        Exceptions:

        """
    
    def add_parameters(self, parameters:list[str]):
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

    def remove_parameter(self, parameter:str):
        """Removes an UmlParameter from the UmlMethod.
        Params:
            name: name of the parameter to remove
        Returns:
            0 if the parameter was successfully removed  
            a number corresponding to an error in the errors class
            if a parameter was not removed form the class
        Exceptions:
            
        """
    
    def rename_parameter(self, parameter:str, newname:str):
        """Renames an UmlParameter from the UmlMethod.
        Params:
            name: name of the parameter to rename
            new: the new name of the parameter
        Returns:
            0 if the parameter was successfully renamed  
            a number corresponding to an error in the errors class
            if a parameter was not removed form the class
        Exceptions:
            
        """
    
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
