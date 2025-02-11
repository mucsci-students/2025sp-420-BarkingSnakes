# Filename: attribute.py
# Authors: John Hershey, Kyle kalbach
# Date 2-5/2025
# Description: class for object attribute methods and design

import logging
from dataclasses import dataclass
import errors

@dataclass
class Attribute:
    attrName:str

    def __init__(self, name):
        self.attrName = name

    def rename_Attr(self,name:str) -> int:
        """Renames the Attribute
        Params: 
            name: new name for the Attribute
        Returns:
            0: if the Attribute was successfully renamed
            -1:if Attribute was not renamed
        Exceptions:
            UMLException if the new name is invalid or duplicate
        """""
        #this should be caught in uml
        try:
            errors.validName(name)
            self.class_name = name
            return 0
        except Exception as e:
            logging.log(0,f"error name is {e.name}, num={e.errorNum}")
            return -1