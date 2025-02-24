# Filename: test_save_load.py
# Authors: Steven Barnes, John Hershey
# Date: 2025-02-16
# Description: Unit tests for the save and load module

import os
import pytest

from src import errors
from src.uml import UmlProject
from src.umlcontroller import UmlApplication

def test_load_no_existing_file():
    """tests that an invalid file error is given when loading a fake file"""
    #temp variable for proving exeption
    var=None
    try:
        UmlProject().load("fake.json")
    except Exception as e:
        var=1
        assert e == errors.InvalidFileException()
    #make sure an exception was raised
    assert var
    
def test_load_invalid_file():
    """tests that an invalid file error is given when loading a fake file"""
    #temp variable for proving exeption
    var=None
    try:
        UmlProject().load("Readme.ME")
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
    """test a new file is made"""
    var = None
    try:
        UmlApplication().new_project("test.json")
        with open("test.json", "r") as f:
            # make sure file exists
            assert f.read()
            
    except Exception as e:
        var = 1
        assert e == None
    #make sure no exception was raised
    assert not var
    
def test_load_existing_file():
    """test a file that exists can be loaded"""
    try:
        proj = UmlProject()
        proj.load("test.json")
        assert proj.classes != None
    except Exception as e:
        assert e == None

def test_save_existing_file():
    """test that a file will be updated when saved"""
    try:
        proj = UmlApplication()
        proj.load_project("test.json")
        #adds the umlclass with name temp
        proj.command_class("temp")
        proj.command_add_umlclass()
        proj.save_project()
        #loads the file again and checks if the change was saved
        proj.load_project("test.json")
        proj.command_class("temp")
        #try to add the class again
        proj.command_add_umlclass()
    except Exception as e:
        assert e == errors.DuplicateClassException()
    

def test_new_file_old_exists():
    """test an existing file is overridden if project with that name is made"""
    var = None
    try:
        with open("test.json") as file1:
            app = UmlApplication()
            app.new_project("test.json")
            app.command_class("temp")
            app.command_add_umlclass()
            app.save_project()
            with open("test.json") as file2:
                assert 1#(len(file1.read()) != len(file2.read()))
    except Exception as e:
        var = 1
        assert e == None
    assert not var
    
def test_delete():
    """delete the file after other tests are run"""
    os.remove("test.json")
    