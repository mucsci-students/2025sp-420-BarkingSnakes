# Filename: attribute.py
# Authors: John Hershey
# Date 2025-02-07
# Description: class listing errors
import keyword
#predeclaration of class
class UMLException(Exception):()

#object methods
class UMLException(Exception):
    """
    Exception wrapper class for the UML
        Declaration Params:   
            name: error name
        Variables:
            name: name of error
            error_num: number of the error
        Exceptions:
            NoSuchErrorError: if error name not in error_list
    """
    
    def equals(self, other:UMLException):
        """checks if self and other have the same error num"""
        return self.error_num == other.error_num
    
    def __eq__(self,other:UMLException):
        """checks if self and other have the same error num, using =="""
        return self.error_num == other.error_num
    
    def __init__(self, *args):
        """initializes the error name and error number"""
        #initalize superclass as well
        super().__init__(*args)
        #set name to specifed error
        self.name = args[0]
        #only add the number if specified
        if self.name in error_list:
            self.error_num = error_list[self.name]
        #raise error if error not in list
        else:
            raise UMLException("NoSuchErrorError")
    
    def get_name(self) -> str:
        """
        Gets name of the error
            Params:   
                None
            Returns:
                name: name of exception
        """
        return self.name
    def get_num(self) -> int:
        """
        Gets number of the error
            Params:   
                None
            Returns:
                errorNum: number of exception
        """
        return self.error_num
#class objects to prevent from being used
uml_names = ["attribute", "relation", "exit", "quit", "help", "name", "list", 
             "back", "add", "delete", "rename", "umlclass", "", " "]
#adds python keywords to list of invalid works
invalid_names = uml_names + keyword.kwlist
error_list = {
    "NoSuchErrorError":0,
    "NullObjectError":1,
    "InvalidNameError":2,
    "DuplicateClassError":3,
    "NoSuchObjectError":4,
    "NoActiveProjectError":5,
    "NoActiveClassError":6,
    "DuplicateAttributeError":7,
    "InvalidFileError":8
}

#class methods
def valid_name(name:str) -> int:
    """
    Checks if a class name is valid
        Params: 
            name: potential name in the uml, a string
        Returns:
            0: if name was not an invalid keyword
        Exceptions:
            InvalidNameError: if the name is invalid
    """
    if name.lower() in invalid_names:
        raise UMLException("InvalidNameError")
    return 0

def get_error_name(val:int) -> str:
    """
    returns the name for a given error in the error_list dict
        Params:   
            val: the error value to find the corresponding name for
        Returns:
            error_name: the error name with the number from input
    """
    #if out of range give that error
    if val < 0 or val >= len(error_list):
        raise UMLException("NoSuchErrorError")
    # takes the list of keys, and finds the error name at val
    error_name = list(error_list.keys())[val]
    return error_name

class NullObjectException(UMLException):
    """
    Wrapper of UMLException class for null object error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    def __init__(self, *args):
        super().__init__(get_error_name(1),*args)

class InvalidNameException(UMLException):
    """
    Wrapper of UMLException class for invalid name error
        Args:
            None: Error automatically passes its name
            onto UMLException so no args are needed
    """
    def __init__(self, *args):
        super().__init__(get_error_name(2),*args)
        
class DuplicateClassException(UMLException):
    """
    Wrapper of UMLException class for duplicate class error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    def __init__(self, *args):
        super().__init__(get_error_name(3),*args)

class NoSuchObjectException(UMLException):
    """
    Wrapper of UMLException class for no such object error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    def __init__(self, *args):
        super().__init__(get_error_name(4),*args)

class NoActiveProjectException(UMLException):
    """
    Wrapper of UMLException class for no active project error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    def __init__(self, *args):
        super().__init__(get_error_name(5),*args)

class NoActiveClassException(UMLException):
    """
    Wrapper of UMLException class for no active class error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    def __init__(self, *args):
        super().__init__(get_error_name(6)*args)

class DuplicateAttributeException(UMLException):
    """
    Wrapper of UMLException class for duplicate attribute error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    def __init__(self, *args):
        super().__init__(get_error_name(7),*args)

class InvalidFileException(UMLException):
    """
    Wrapper of UMLException class for invalid file error
        Args:
            None: Error automatically passes its name onto
            UMLException so no args are needed
    """
    def __init__(self, *args):
        super().__init__(get_error_name(8),*args)