# Filename: test_save_load.py
# Authors: Steven Barnes, John Hershey
# Date: 2025-02-25
# Description: Unit tests for the save and load module

import os
import pytest

from src import errors
from src.umlmodel import UmlProject
from src.umlcontroller import UmlApplication, UmlController
from src.views.umlview_cli import UmlCliView

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
    """tests that an invalid file error is given when loading a non-json file"""
    #temp variable for proving exeption
    var=None
    try:
        UmlProject().load("Readme.ME")
    except Exception as e:
        var=1
        assert e == errors.InvalidFileException()
    #make sure an exception was raised
    assert var

def test_make_no_new_file():
    """test a new file was not made"""
    var = None
    try:
        # app = UmlApplication()
        app = UmlController(UmlCliView())
        app.new_project("test.json")
        with open("test.json", "r") as f:
            # make sure file doesn't exists
            assert not f.read()
            
    except Exception as e:
        var = 1
        assert e.__class__ == FileNotFoundError
    #make sure an exception was raised
    assert var

def test_save_no_existing_file():
    """test that no error is given when saving to a 
        filename that does not yet exist"""
    var = None
    proj = UmlProject()
    try:
        proj._save_path = "test.json"
        #save does not need a filename if path is already set
        proj.save()
        assert os.path.exists("test.json")
    except Exception as e:
        var = 1
        assert e == None
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
    var = 1
    try:
        # app = UmlApplication()
        app = UmlController(UmlCliView())
        app.load_project("test.json")
        #adds the umlclass with name temp
        # app.active_class = "temp"
        app.command_add_umlclass("temp")
        app.model.save()
        assert "temp" in app.model.classes
        var = 2
        #loads the file again and checks if the change was saved
        app.load_project("test.json")
        # app.command_class("temp")
        #try to add the class again
        app.command_add_umlclass("temp")
        var = 3
    except Exception as e:
        var = None
        assert e == errors.DuplicateClassException()
    
    assert not var
    
def test_new_old_file_exists():
    """test an existing file is not overridden 
    when project with that name is made, only when saved"""
    var = None
    try:
        # app = UmlApplication()
        app = UmlController(UmlCliView())
        app.new_project("test.json")
        #another app to check file state
        # app2 = UmlApplication()
        app2 = UmlController(UmlCliView())
        app2.load_project("test.json")
        #assert class remains
        assert "temp" in app2.model.classes
        # app-level save prompts user, so until prints are handled by
        # tests - a view-implementation-solvable issue, use project save
        app.model.save()
        app2.load_project("test.json")
        assert "temp" not in app2.model.classes
    except Exception as e:
        var = 1
        assert e == None
    assert not var
    
def test_delete():
    """delete the file after other tests are run"""
    os.remove("test.json")
    