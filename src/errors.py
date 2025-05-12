# Filename: errors.py
# Authors: John Hershey, Evan Magill, Steven Barnes
# Creation Date 2025-02-25. Last Edit Date: 2025-05-12
# Description: class listing errors

## imports
from __future__ import annotations
import re

## static class objects
REGEX_DEFAULT_PATTERN = "^[A-Za-z][A-Za-z0-9_]*$"

## class definitions
class UMLException(Exception):
    """
    Exception wrapper class for the UML
        contains equality method for comparing different errors
    """
    
    def equals(self, other:UMLException):
        """checks if self and other have the same class"""
        #no need for error_list since this gets the name from the name of the error's class
        return self.__class__.__name__ == other.__class__.__name__

    def __eq__(self,other:UMLException):
        """checks if self and other are the same error"""
        return self.__class__.__name__ == other.__class__.__name__

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

### error classes
# nothing is specifed other than the docstring by default
# since the basic init works for most
class NoSuchErrorException(UMLException):
    """
    Wrapper of UMLException class for "no such error" error
        Args:
            None
    """

class NullObjectException(UMLException):
    """
    Wrapper of UMLException class for null object error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """

class InvalidNameException(UMLException):
    """
    Wrapper of UMLException class for invalid name error
        Args:
            None: Error automatically passes its name
            onto UMLException so no args are needed
    """
        
class DuplicateClassException(UMLException):
    """
    Wrapper of UMLException class for duplicate class error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """

class NoSuchObjectException(UMLException):
    """
    Wrapper of UMLException class for no such object error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    #kwargs is keyword-specified variables
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.object_type = kwargs.get("object_type")

class NoActiveProjectException(UMLException):
    """
    Wrapper of UMLException class for no active project error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """

class NoActiveClassException(UMLException):
    """
    Wrapper of UMLException class for no active class error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """

class DuplicateFieldException(UMLException):
    """
    Wrapper of UMLException class for duplicate field error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """

class InvalidFileException(UMLException):
    """
    Wrapper of UMLException class for invalid file error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
        
class DuplicateRelationshipException(UMLException):
    """
    Wrapper of UMLException class for duplicate relationship error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """

class DuplicateMethodOverloadException(UMLException):
    """exception for when a new method overload already exists"""

class MethodNameNotExistsException(UMLException):
    """exception for when a named method does not exist"""

class MethodOverloadNotExistsException(UMLException):
    """exception for when a specific method overload does not exist"""

class DuplicateParameterException(UMLException):
    """exception for when a new parameter name already exists"""

class NoSuchParameterException(UMLException):
    """exception for when a named parameter does not exist"""

class InvalidJsonSchemaException(UMLException):
    """exception for when a loaded file does not match the template saved pattern"""

class NoActiveMethodException(UMLException):
    """exception for when a method command is attempted outside method context"""

class InvalidRelationshipTypeException(UMLException):
    """exception for invalid type name of fields, methods, and parameters"""

class FileAlreadyExistsException(UMLException):
    """exception for when a file exists with the same name as a new save object"""

class FileHasUnsavedChangesException(UMLException):
    """exception for when the project has unsaved changes"""

class InvalidTypeNameException(UMLException):
    """exception for invalid type name of fields, methods, and parameters"""
        
class TestViewPromptException(UMLException):
    """
    Wrapper of UMLException class for testing user input\n\
        if prompt would normally be given, this error is raised,\n\
        with the intended prompt given as an arg for the testing file to handle
    Args:
        prompt: the intended prompt for the user. This does not need to be included
    """
    def __init__(self, *args):
        super().__init__(*args)
        self.prompt = args[0]
        
class InvalidPositionArgsException(UMLException):
    """exception for invalid position arguments"""
    
class NoActionsLeftException(UMLException):
    """exception for redo and undo failing due to no actions left to revert"""