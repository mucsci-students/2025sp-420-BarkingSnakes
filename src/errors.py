# Filename: attribute.py
# Authors: John Hershey
# Date 2-7/2025
# Description: class listing errors
import keyword
InvalidNames = ["class","attribute", "relation"]
InvalidNames += keyword.kwlist
errorList = {
        "NullObjectError":1,
        "InvalidNameError":2
        }
class UMLException(Exception):
    InvalidObjectNameException = 2
    def __init__(self, *args):
        #initalize superclass as well
        super().__init__(*args)
        #set name to specifed error
        self.name = args[0]
        #only add the number if specified
        self.errorNum = errorList[self.name]

    def validName2(self,name):
        if name.lower() in self.InvalidNames:
            return 2

def validName(name):
        if name.lower() in InvalidNames:
            raise UMLException("InvalidNameError")
def noClass(classObj):
    if classObj == None:
        raise UMLException("NullObjectError")
