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
        Declaration Params:   
            name: error name
        Variables:
            error_num: number of the error
        Exceptions:
            NoSuchErrorError: if error name not in error_list
    """
    
    def equals(self, other:UMLException):
        """checks if self and other have the same error num"""
        return self.error_num == other.error_num

    def __eq__(self,other:UMLException):
        """checks if self and other have the same error num, using =="""
        return self.__class__ == other.__class__
        #return self.error_num == other.error_num
    
    def __init__(self, num, *args):
        """
        initializes the error number of the specific error
            args allows for more description if needed
        """
        #initalize superclass as well
        super().__init__(*args)
        #add the number
        self.error_num = num

    def get_num(self) -> int:
        """
        Gets number of the error
            Params:   
                None
            Returns:
                errorNum: number of exception
        """
        return self.error_num

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
class NullObjectException(UMLException):
    """
    Wrapper of UMLException class for "no such error" error
        Args:
            None
    """
    def __init__(self, *args):
        super().__init__(0,*args)

class NullObjectException(UMLException):
    """
    Wrapper of UMLException class for null object error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    def __init__(self, *args):
        super().__init__(1,*args)

class InvalidNameException(UMLException):
    """
    Wrapper of UMLException class for invalid name error
        Args:
            None: Error automatically passes its name
            onto UMLException so no args are needed
    """
    def __init__(self, *args):
        super().__init__(2,*args)
        
class DuplicateClassException(UMLException):
    """
    Wrapper of UMLException class for duplicate class error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    def __init__(self, *args):
        super().__init__(3,*args)

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
    def __init__(self, *args):
        super().__init__(5,*args)

class NoActiveClassException(UMLException):
    """
    Wrapper of UMLException class for no active class error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    def __init__(self, *args):
        super().__init__(6, *args)

class DuplicateFieldException(UMLException):
    """
    Wrapper of UMLException class for duplicate field error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    def __init__(self, *args):
        super().__init__(7,*args)

class InvalidFileException(UMLException):
    """
    Wrapper of UMLException class for invalid file error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    def __init__(self, *args):
        super().__init__(8,*args)
        
class DuplicateRelationshipException(UMLException):
    """
    Wrapper of UMLException class for duplicate relationship error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    def __init__(self, *args):
        super().__init__(9,*args)

class DuplicateMethodOverloadException(UMLException):
    def __init__(self, *args):
        super().__init__(10, *args)

class MethodNameNotExistsException(UMLException):
    def __init__(self, *args):
        super().__init__(11, *args)

class MethodOverloadNotExistsException(UMLException):
    def __init__(self, *args):
        super().__init__(12, *args)

class DuplicateParameterException(UMLException):
    def __init__(self, *args):
        super().__init__(13, *args)

class NoSuchParameterException(UMLException):
    def __init__(self, *args):
        super().__init__(14, *args)

class InvalidJsonSchemaException(UMLException):
    def __init__(self, *args):
        super().__init__(15, *args)

class NoActiveMethodException(UMLException):
    def __init__(self, *args):
        super().__init__(16, *args)

class InvalidRelationshipTypeException(UMLException):
    def __init__(self, *args):
        super().__init__(17, *args)

class FileAlreadyExistsException(UMLException):
    def __init__(self, *args):
        super().__init__(18, *args)

class FileHasUnsavedChangesException(UMLException):
    def __init__(self, *args):
        super().__init__(19, *args)

class UmlClassDeletionErrorException(UMLException):
    def __init__(self, *args):
        super().__init__(20, *args)

class InvalidTypeNameException(UMLException):
    def __init__(self, *args):
        super().__init__(21,*args)
        
class TestViewPromptException(UMLException):
    """
    Wrapper of UMLException class for testing user input\n\
        if prompt would normally be given, this error is raised,\n\
        with the intended prompt given as an arg for the testing file to handle
    Args:
        prompt: the intended prompt for the user. This does not need to be included
    """
    def __init__(self, *args):
        super().__init__(22,*args)
        
class InvalidPositionArgsException(UMLException):
    """exception for invalid position arguments"""
    def __init__(self, *args):
        super().__init__(23,*args)