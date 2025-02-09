# Filename: umlclass.py
# Authors: Kyle Kalbach
# Date: 02-07-2025
# Description: umlclass methods
from dataclasses import dataclass
from attribute import Attribute
import keyword

@dataclass
class UmlClass:
    class_name:str
    class_attributes:dict[str,Attribute]

    def add_attribute(self,attribute:Attribute) -> int:
        """Adds an attribute to the UmlClass
        Returns:
            0 if attribute added to the class\n
            a number corresponding to an error in the errors class
            if attribute was not added to class
        """ 
        if attribute.name in self.class_attributes.keys():
            #return error code or handle existing key
            return -1
        self.class_attributes[attribute.name] = attribute
        return 0

    def remove_attribute(self,name:str) -> int:
        """Removes an Attribute from the UmlClass
        Params:
            name: name of the attribute to remove
        Returns:
            0: if the attribute was successfully removed
            a number corresponding to an error in the errors class
            if an attribute was not removed form the class
        """
        if name not in self.class_attributes.keys():
            #return error code for nonexistent attribute    
            return -1
        self.class_attributes.pop(name)
        return 0
    
    def rename_umlclass(self,name:str) -> int:
        """Renames the UmlClass
        Params: 
            name: new name for the class
        Returns:
            0: if the class was successfully renamed
            a number corresponding to an error in the errors class
            if the UmlClass was not renamed
        """
        if keyword.iskeyword(name):
            #return errorcode for name param is python keyword
            return -1
        self.class_name = name
    