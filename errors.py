# Filename: attribute.py
# Authors: John Hershey
# Date 2-7/2025
# Description: class listing errors
InvalidNames = ["class","attribute"]
class UMLException(Exception):
    InvalidNames2 = ["class","attribute"]
    InvalidObjectNameException = 2
    
    def validName2(self,name):
        if name.lower() in self.InvalidNames:
            return 2

def validName(name):
        if name.lower() in InvalidNames:
            raise UMLException
