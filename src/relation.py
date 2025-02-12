# Filename: attribute.py
# Authors: John Hershey, Kyle kalbach
# Date 2-5/2025
# Description: class for object relationships methods and design

import logging
from dataclasses import dataclass
import errors

@dataclass
class Relation:
    source:str
    dest:str

    def __init__(self, src_name, des_name):
        self.source = src_name
        self.dest = des_name

    def del_rel(self,name:str) -> int:
        """
        
        """
        errors.valid_name(name)
        self.class_name = name
        return 0