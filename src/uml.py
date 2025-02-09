# Filename: uml.py
# Authors: Steven Barnes
# Date: 2025-02-02
# Description: Entry point for UML editor program.

import os
import json
import sys
import re

def load(fpath:str) -> dict:
    """Read data from the provided .json file.
    :param fpath: String containing the full path to the .json file.
    :return: 
    """

    error_dict = {"error": "Invalid file path."}

    if not os.path.exists(fpath):
        return error_dict
    
    if not os.path.isfile(fpath):
        return error_dict
    
    if not re.search('\.json', fpath, flags=re.IGNORECASE):
        return error_dict

    with open(fpath, "r") as f:
        return json.load(f)

class UML_Class:
    """"""

    def __init__(self, name:str, attributes):
        """"""
        self.name = name
        self.attributes = attributes

class UML_Project:
    """"""

    def __init__(self, classes:list[UML_Class]):
        """"""
        self.classes = classes

def setup_program():
    """Validates requirements for the program are met before attempting to start."""


def main():
    """Entry point for the program."""

if __name__ == "__main__":
    main()