# Filename: test_umlmodel.py
# Authors: Steven Barnes, John Hershey, Evan Magill, Kyle Kalbach, Juliana Vinluan, Spencer Hoover
# Creation Date: 04-06-2025, Last Edit Date: 04-06-2025
# Description: Unit Tests for umlmodel.py
import os
import sys
import logging

from src.umlclass import UmlClass
from src.umlfield import UmlField
from src.umlmethod import UmlMethod
from src.umlparameter import UmlParameter
from src.umlmodel import UmlProject
from src import errors

def test_rename_umlclass():
    """Tests rename umlclass"""
    test_proj = UmlProject()
    test_proj.add_umlclass("testclass")

    test_proj.rename_umlclass("testclass","testclass2")

    assert "testclass2" in test_proj.classes

def test_rename_umlclass_nonexistant_class():
    """Tests rename umlclass nosuchobjecterror"""
    test_proj = UmlProject()
    test_proj.add_umlclass("testclass")

    try:
        test_proj.rename_umlclass("testclass1","testclass2")
    except Exception as e:
        test_val_error = e.get_num()
    finally:
        assert test_val_error == errors.error_list["NoSuchObjectError"]

def test_rename_umlclass_existing_class():
    """Tests rename umlclass duplicateclasserro"""
    test_proj = UmlProject()
    test_proj.add_umlclass("testclass")
    test_proj.add_umlclass("car")

    try:
        test_proj.rename_umlclass("testclass","car")
    except Exception as e:
        test_val_error = e.get_num()
    finally:
        assert test_val_error == errors.error_list["DuplicateClassError"]

def test_delete_umlclass():
    """Tests delete_umlclass"""
    test_proj = UmlProject()
    test_proj.add_umlclass("car")
    test_proj.delete_umlclass("car")

    assert "car" not in test_proj.classes

def test_delete_umlclass_nonexistant_class():
    """Tests delete_umlclass"""
    test_proj = UmlProject()
    test_proj.add_umlclass("car")
    
    try:
        test_proj.delete_umlclass("van")
    except Exception as e:
        test_val_error = e.get_num()
    finally:
        assert test_val_error == errors.error_list["NoSuchObjectError"]
    
def test_add_field():
    """Tests add_field"""
    test_proj = UmlProject()
    test_proj.add_umlclass("car")
    test_proj.add_field("car","MaxSpeed","mph")
    
    test_class = test_proj.classes.pop("car")

    assert "MaxSpeed" in test_class.class_fields

def test_add_field():
    """Tests add_field"""
    test_proj = UmlProject()
    test_proj.add_umlclass("car")
    test_proj.add_field("car","MaxSpeed","mph")
    
    try:
        test_proj.add_field("car","MaxSpeed","mph")
    except Exception as e:
        test_val_error = e.get_num()
    finally:
        assert test_val_error == errors.error_list["DuplicateFieldError"]

def test_rename_field():
    """Tests rename_field"""
    test_proj = UmlProject()
    test_proj.add_umlclass("car")
    test_proj.add_field("car","MaxSpeed","mph")

    test_proj.rename_field("car","MaxSpeed","MinSpeed")

    assert "MinSpeed" in  test_proj.classes.get("car").class_fields
    assert "MaxSpeed" not in  test_proj.classes.get("car").class_fields

def test_delete_field():
    """Tests delete_field"""
    test_proj = UmlProject()
    test_proj.add_umlclass("car")
    test_proj.add_field("car","MaxSpeed","mph")

    test_proj.delete_field("car","MaxSpeed")

    assert "MaxSpeed" not in  test_proj.classes.get("car").class_fields


    
