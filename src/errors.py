# Filename: attribute.py
# Authors: John Hershey
# Date 2025-02-07
# Description: class listing errors
import keyword
class UMLException(Exception):()

#object methods
class UMLException(Exception):
    """
    Exception wrapper class for the UML
        Declaration Params:   
            name: error name
        Variables:
            <case:description>
        Exceptions:
            <exception type:reason>
    """
    def __init__(self, *args):
        #initalize superclass as well
        super().__init__(*args)
        #set name to specifed error
        self.name = args[0]
        #only add the number if specified
        if self.name in errorList:
            self.errorNum = errorList[self.name]
        #default to -1 if not in list
        else:
            self.errorNum = -1
    
    def getName(self) -> str:
        """
        Gets name of the error
            Params:   
                None
            Returns:
                name: name of exception
        """
        return self.name
    def getNum(self) -> int:
        """
        Gets number of the error
            Params:   
                None
            Returns:
                errorNum: number of exception
        """
        return self.errorNum
#class objects
umlNames = ["attribute", "relation", "exit", "quit", "help"
            , "name","", " "]
InvalidNames = umlNames + keyword.kwlist
errorList = {
    "NullObjectError":1,
    "InvalidNameError":2,
    "DuplicateNameError":3,
    "NoSuchObjectError":4
}

#class methods
def validName(name:str) -> int:
    """
    Checks if a class name is valid
        Params: 
            name: potential name in the uml, a string
        Returns:
            0: if name was not an invalid keyword
        Exceptions:
            InvalidNameError: if the name is invalid
    """
    if name.lower() in InvalidNames:
        raise UMLException("InvalidNameError")
    return 0
def noClass(classObj):
    """
    don't use, simply throw no class error
        Params:   
            <input:description>
        Returns:
            <case:description>
        Exceptions:
            <exception type:reason>
    """
    if classObj == None:
        raise UMLException("NullObjectError")
    #else if classObj.type != umlclass.UmlClass:
    #    return -1
    return 0
