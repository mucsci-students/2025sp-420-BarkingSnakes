# Filename: attribute.py
# Authors: John Hershey
# Date 2-7/2025
# Description: class listing errors
import keyword
class UMLException(Exception):()

#object methods
class UMLException(Exception):
    def __init__(self, *args):
        #initalize superclass as well
        super().__init__(*args)
        #set name to specifed error
        self.name = args[0]
        #only add the number if specified
        self.errorNum = errorList[self.name]

    def validName(self,name):
        if name.lower() in InvalidNames:
            return 2
        
#class objects
InvalidNames = ["attribute", "relation", "exit", "quit"]
InvalidNames += keyword.kwlist
errorList = {
        "NullObjectError":1,
        "InvalidNameError":2,
        "DuplicateNameError":3,
        "NoSuchObjectError":4
        }

#class methods
def validName(name:str):
    """checks if a class name is valid
    Params: 
        name: name for the class
    Returns:
        0: if name was valid
        InvalidNameError: if name was invalid
    Exceptions:
            UMLException if the new name is invalid
    """
    if name.lower() in InvalidNames:
        raise UMLException("InvalidNameError")
    return 0
def noClass(classObj):
    if classObj == None:
        raise UMLException("NullObjectError")
    #else if classObj.type != umlclass.UmlClass:
    #    return -1
    return 0
