# Filename: umlclass.py
# Authors: Kyle Kalbach, Steven Barnes, Evan Magill
# Date: 2025-02-16
# Description: umlclass methods
import logging
from dataclasses import dataclass
from umlfield import UmlField
import errors

@dataclass
class UmlClass:
    class_name:str
    class_fields:dict[str, UmlField]

    def add_field(self,name:str) -> int:
        """
        Adds an field to the UmlClass
            Returns:
                0: if field added to the class
            Exceptions:
                DuplicateFieldError: if name exists
                InvalidNameError: if name invalid
        """ 
        if name in self.class_fields.keys():
            #return error code or handle existing key
            raise errors.DuplicateFieldException()
        errors.valid_name(name)
        self.class_fields[name] = UmlField(name)
        return 0

    def remove_field(self,name:str) -> int:
        """Removes an field from the UmlClass
        Params:
            name: name of the field to remove
        Returns:
            0: if the field was successfully removed
            a number corresponding to an error in the errors class
            if an field was not removed from the class
        """
        if name not in self.class_fields.keys():
            #return error code for nonexistent field
            raise errors.NoSuchObjectException()
        self.class_fields.pop(name)
        return 0
    
    def rename_field(self,oldname:str,newname:str) -> int:
        """Renames the specified field
        Params: 
            oldname: existing field to rename
            newname: name to replace oldname
        Returns:
            0: if the field was successfully renamed
        Exceptions:
            UMLException:InvalidNameError if the new name is invalid
            UMLException:NoSuchObjectError if the field does not exist
            UMLException:DuplicateFieldError if newname exist in class_fields
        """
        errors.valid_name(newname)

        if newname in self.class_fields.keys():
            #return error code or handle existing key
            raise errors.DuplicateFieldException()
        
        self.class_fields.pop(oldname)
        self.add_field(newname)
        return 0

    def rename_umlclass(self,name:str) -> int:
        """
        Renames the UmlClass
        Params: 
            name: new name for the class
        Returns:
            0: if the class was successfully renamed
        Exceptions:
            UMLException:InvalidNameError if the new name is invalid
            UMLException:NoSuchObjectError if the class does not exist
        """
        # method will throw exception for parent to catch 
        # if name is invalid
        errors.valid_name(name)
        self.class_name = name
        return 0
            
        
    