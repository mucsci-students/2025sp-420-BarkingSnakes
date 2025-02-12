# Filename: umlclass.py
# Authors: Kyle Kalbach, Steven Barnes, Evan Magill
# Date: 02-07-2025
# Description: umlclass methods
import logging
from dataclasses import dataclass
from attribute import Attribute
from umlrelationship import UmlRelationship
import errors

@dataclass
class UmlClass:
    class_name:str
    class_attributes:dict[str,Attribute]
    class_relationships:list[UmlRelationship]

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
    
    def has_relationship(self, relationship:UmlRelationship):
        return relationship in self.class_relationships

    def add_relationship(self, relationship:UmlRelationship):
        """Adds a UmlRelationship to the class
        Params:
            relationship: the UmlRelationship object to be added.
        Returns:
            0: if the relationship was successfully added to the class.
            -1: if a failure occurred. Some fundamental Python problem.
        """
        try:
            self.class_relationships.append(relationship)
        except:
            return -1 # appending to a list failed?
        return 0

    def rename_umlclass(self,name:str) -> int:
        """Renames the UmlClass
        Params: 
            name: new name for the class
        Returns:
            0: if the class was successfully renamed
            -1:if UmlClass was not renamed
        Exceptions:
            UMLException if the new name is invalid or duplicate
        """
        try:
            errors.validName(name)
            self.class_name = name
            return 0
        except Exception as e:
            logging.log(0,f"error name is {e.name}, num={e.errorNum}")
            return -1
            
        
    