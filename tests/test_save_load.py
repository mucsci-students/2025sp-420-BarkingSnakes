# Filename: test_save_load.py
# Authors: Steven Barnes
# Date: 2025-02-08
# Description: Unit tests for the save and load module

import os

from src.uml import UmlProject

def test_no_existing_file():
    fpath = os.path.join("this_file_doesnt_exist.json")

