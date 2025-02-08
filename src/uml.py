# Filename: uml.py
# Authors: Steven Barnes
# Date: 2025-02-02
# Description: Entry point for UML editor program.

import os
import json
import sys
#run this for cross folder linking
if os.path.abspath('..') not in sys.path:
    sys.path.append(os.path.abspath('..'))
print(sys.path)
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