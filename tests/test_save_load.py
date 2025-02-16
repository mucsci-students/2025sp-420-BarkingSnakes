# Filename: test_save_load.py
# Authors: Steven Barnes
# Date: 2025-02-08
# Description: Unit tests for the save and load module

import os
import pytest

from src import errors
from src.uml import UmlProject

def test_load_no_existing_file():
    """tests that an invalid file error is given when loading a fake file"""
    var=None
    try:
        UmlProject().load("fake.json")
    except Exception as e:
        var=1
        assert e == errors.InvalidFileException()
    #make sure an exception was raised
    assert var
    
def test_save_no_existing_file():
    """test that a no active project error is given when saving with no file"""
    var = None
    proj = UmlProject()
    try:
        proj.save()
    except Exception as e:
        var = 1
        assert e == errors.NoActiveProjectException()
    assert var

def test_make_new_file():
    """test that a no active project error is given when saving with no file"""
    var = None
    proj = UmlProject()
    
def test_load_existing_file():
    """test that a no active project error is given when saving with no file"""
    var = None
    proj = UmlProject()

def test_save_existing_file():
    """test that a no active project error is given when saving with no file"""
    var = None
    proj = UmlProject()
    
    
#def test_file_was_created():
    #"""make sure file exists to delete"""
    #os.remove("temp.json")
    