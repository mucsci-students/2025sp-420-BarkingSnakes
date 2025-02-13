# Filename: test_save_load.py
# Authors: Steven Barnes
# Date: 2025-02-08
# Description: Unit tests for the save and load module

import os

from src.errors import UMLException
from src.uml import UmlProject


def test_load_no_existing_file():
    #try:
        #UmlProject.load(UmlProject,"fake.json")
    #except UMLException as e:
        # 8 corresponds to InvalidFileError in the error list
        #assert e.get_num == 8
    fpath = os.path.join("this_file_doesnt_exist.json")
    

