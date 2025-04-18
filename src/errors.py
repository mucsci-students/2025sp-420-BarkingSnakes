# Filename: errors.py
# Authors: John Hershey, Evan Magill, Steven Barnes
# Creation Date 2025-02-25. Last Edit Date: 2025-04-18
# Description: class listing errors

## imports
from __future__ import annotations
import re

## static class objects
REGEX_DEFAULT_PATTERN = "^[A-Za-z][A-Za-z0-9_]*$"

error_list = {
    "NoSuchErrorError":0,
    "NullObjectError":1,
    "InvalidNameError":2,
    "DuplicateClassError":3,
    "NoSuchObjectError":4,
    "NoActiveProjectError":5,
    "NoActiveClassError":6,
    "DuplicateFieldError":7,
    "InvalidFileError":8,
    "DuplicateRelationshipError":9,
    "DuplicateMethodOverloadError":10,
    "MethodNameNotExistsError":11,
    "MethodOverloadNotExistsError":12,
    "DuplicateParameterError":13,
    "NoSuchParameterError":14,
    "InvalidJsonSchemaError":15,
    "NoActiveMethodError":16,
    "InvalidRelationshipTypeError":17,
    "FileAlreadyExistsError": 18,
    "FileHasUnsavedChangesError": 19,
    "UmlClassDeletionError": 20,
    "InvalidTypeNameError": 21,
    "TestViewPromptError": 22,
    "InvalidPositionArgsError":23
}
## class definitions
class UMLException(Exception):
    """
    Exception wrapper class for the UML
        contains equality method for comparing different errors
    """
    
    def equals(self, other:UMLException):
        """checks if self and other have the same error num"""
        return self.__class__ == other.__class__

    def __eq__(self,other:UMLException):
        """checks if self and other have the same error num, using =="""
        return self.__class__ == other.__class__
        #return self.error_num == other.error_num
    
    def __init__(self, *args):
        """
        args allows for more description if needed
        """
        #initalize superclass as well
        super().__init__(*args)

#class methods
def valid_name(name:str, regex:str = REGEX_DEFAULT_PATTERN):
    """
    Checks if a class name is valid
        Params: 
            name: potential name in the uml, a string
        Returns:
            None
        Exceptions:
            InvalidNameError: if the name is invalid
    """
    if re.search(regex, name) is None:
        raise InvalidNameException()
    return

## error types
class NoSuchErrorException(UMLException):
    """
    Wrapper of UMLException class for "no such error" error
        Args:
            None
    """
    args:list

class NullObjectException(UMLException):
    """
    Wrapper of UMLException class for null object error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    args:list

class InvalidNameException(UMLException):
    """
    Wrapper of UMLException class for invalid name error
        Args:
            None: Error automatically passes its name
            onto UMLException so no args are needed
    """
    args:list
        
class DuplicateClassException(UMLException):
    """
    Wrapper of UMLException class for duplicate class error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    args:list

class NoSuchObjectException(UMLException):
    """
    Wrapper of UMLException class for no such object error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    def __init__(self, *args, **kwargs):
        super().__init__(4,*args)
        self.object_type = kwargs.get("object_type")

class NoActiveProjectException(UMLException):
    """
    Wrapper of UMLException class for no active project error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    args:list

class NoActiveClassException(UMLException):
    """
    Wrapper of UMLException class for no active class error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    args:list

class DuplicateFieldException(UMLException):
    """
    Wrapper of UMLException class for duplicate field error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    args:list

class InvalidFileException(UMLException):
    """
    Wrapper of UMLException class for invalid file error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    args:list
        
class DuplicateRelationshipException(UMLException):
    """
    Wrapper of UMLException class for duplicate relationship error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    args:list

class DuplicateMethodOverloadException(UMLException):
    args:list

class MethodNameNotExistsException(UMLException):
    args:list

class MethodOverloadNotExistsException(UMLException):
    args:list

class DuplicateParameterException(UMLException):
    args:list

class NoSuchParameterException(UMLException):
    args:list

class InvalidJsonSchemaException(UMLException):
    args:list

class NoActiveMethodException(UMLException):
    args:list

class InvalidRelationshipTypeException(UMLException):
    args:list

class FileAlreadyExistsException(UMLException):
    args:list

class FileHasUnsavedChangesException(UMLException):
    args:list

class InvalidTypeNameException(UMLException):
    """exception for invalid type name of fields, methods, and parameters"""
    args:list
        
class TestViewPromptException(UMLException):
    """
    Wrapper of UMLException class for testing user input\n\
        if prompt would normally be given, this error is raised,\n\
        with the intended prompt given as an arg for the testing file to handle
    Args:
        prompt: the intended prompt for the user. This does not need to be included
    """
    def __init__(self, *args):
        self.prompt = args[0]
        super().__init__(*args)
        
class InvalidPositionArgsException(UMLException):
    """exception for invalid position arguments"""
    args:list