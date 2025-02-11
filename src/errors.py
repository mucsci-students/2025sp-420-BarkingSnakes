# Filename: attribute.py
# Authors: John Hershey
# Date 2-7/2025
# Description: class listing errors
import keyword

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
            print("test")
            return 2
        
#class objects
InvalidNames = ["attribute", "relation"]
InvalidNames += keyword.kwlist
errorList = {
        "NullObjectError":1,
        "InvalidNameError":2
        }

#class methods
def validName(name):
        if name.lower() in InvalidNames:
            raise UMLException("InvalidNameError")
        return 0
def noClass(classObj):
    if classObj == None:
        raise UMLException("NullObjectError")
