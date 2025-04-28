# Filename: test_umlmodel.py
# Authors: Steven Barnes, John Hershey, Evan Magill, Kyle Kalbach, Juliana Vinluan, Spencer Hoover
# Creation Date: 04-06-2025, Last Edit Date: 04-18-2025
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

# rename class tests
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
        assert False
    except Exception as e:
        assert e == errors.NoSuchObjectException()

def test_rename_umlclass_existing_class():
    """Tests rename umlclass duplicateclasserror"""
    test_proj = UmlProject()
    test_proj.add_umlclass("testclass")
    test_proj.add_umlclass("car")

    try:
        test_proj.rename_umlclass("testclass","car")
        assert False
    except Exception as e:
        assert e == errors.DuplicateClassException()

# delete class tests
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
        assert False
    except Exception as e:
        assert e == errors.NoSuchObjectException()
    
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
        assert False
    except Exception as e:
        assert e == errors.DuplicateFieldException()

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

# update class position tests

def test_update_position_class_no_such_class():
    """Tests that an error is raised if the class isn't in the project"""
    model = UmlProject()
    try:
        model.add_umlclass("temp")
        model.update_position_umlclass("temp2", 1.0, 2.0)
        assert False
    except Exception as e:
        assert e == errors.NoSuchObjectException()
    # make sure existing class wasn't changed
    assert model.get_umlclass("temp").get_umlclass_position() == (0.0, 0.0)
    assert not model.classes.get("temp2")

def test_update_position_class_invalid_type():
    """Tests that an error is raised if a position type isn't float"""
    model = UmlProject()
    try:
        model.add_umlclass("temp")
        model.update_position_umlclass("temp", "str", 2.0)
        assert False
    except Exception as e:
        assert e == errors.InvalidPositionArgsException()
    assert model.get_umlclass("temp").get_umlclass_position() == (0.0, 0.0)
    
def test_update_position_class():
    """Tests that no error is raised if class exists and positions are valid"""
    model = UmlProject()
    try:
        model.add_umlclass("temp")
        model.update_position_umlclass("temp", 1.0, 2.0)
    except Exception as e:
        assert e == None
    assert model.get_umlclass("temp").get_umlclass_position() == (1.0, 2.0)

# get class position tests
def test_get_position_class_no_class():
    """Tests that an error is raised if class does not exist"""
    model = UmlProject()
    try:
        model.add_umlclass("temp")
        model.get_position_umlclass("temp2")
        assert False
    except Exception as e:
        assert e == errors.NoSuchObjectException()
        
def test_get_position_class_exists():
    """Tests that no error is raised if class exists"""
    pos = None
    try:
        model = UmlProject()
        model.add_umlclass("temp")
        model.update_position_umlclass("temp", 1.0, 2.0)
        pos = model.get_position_umlclass("temp")
    except Exception as e:
        assert e == None
    assert pos == (1.0,2.0)

def test_get_umlmethod_exists():
    model = UmlProject()
    model.add_umlclass("temp")
    model.add_method("temp", "method1", "int", [("param1", "string")])

    method = model.get_umlmethod("temp", "method1", "string")

    assert method is not None

def test_get_umlmethod_raises_notexists_exception():
    model = UmlProject()
    model.add_umlclass("temp")

    try:
        model.get_umlmethod("temp", "method1", "string")
    except Exception as e:
        assert e == errors.MethodNameNotExistsException()

def test_get_umlmethod_raises_overloadnotexists_exception():
    model = UmlProject()
    model.add_umlclass("temp")
    model.add_method("temp", "method1", "int", [("param1", "string")])

    try:
        model.get_umlmethod("temp", "method1", "int")
    except Exception as e:
        assert e == errors.MethodOverloadNotExistsException()

def test_add_method():
    model = UmlProject()
    model.add_umlclass("temp")
    model.add_method("temp", "method1", "int", [("param1", "string")])

    method = model.get_umlmethod("temp", "method1", "string")

    assert method is not None

def test_rename_method():
    model = UmlProject()
    model.add_umlclass("temp")
    model.add_method("temp", "method1", "int", [("param1", "string")])

    model.rename_method("temp", "method1", "method2", "string")

    try:
        model.get_umlmethod("temp", "method1", "string")
    except Exception as e:
        assert e == errors.MethodNameNotExistsException()
    
    method = model.get_umlmethod("temp", "method2", "string")

    assert method is not None

def test_delete_method():
    model = UmlProject()
    model.add_umlclass("temp")
    model.add_method("temp", "method1", "int", [("param1", "string")])

    model.delete_method("temp", "method1", "string")

    try:
        model.get_umlmethod("temp", "method1", "string")
    except Exception as e:
        assert e == errors.MethodNameNotExistsException()

def test_add_parameter():
    model = UmlProject()
    model.add_umlclass("temp")
    model.add_method("temp", "method1", "int", [("param1", "string")])

    model.add_parameter("temp", "method1", "string", "param2", "int")

    try:
        model.get_umlmethod("temp", "method1", "string")
    except Exception as e:
        assert e == errors.MethodOverloadNotExistsException()
    
    method = model.get_umlmethod("temp", "method1", "string int")

    assert method is not None

def test_rename_parameter():
    model = UmlProject()
    model.add_umlclass("temp")
    model.add_method("temp", "method1", "int", [("param1", "string")])

    model.rename_parameter("temp", "method1", "string", "param1", "param2")

    method = model.get_umlmethod("temp", "method1", "string")

    assert len(method.params) == 1 and method.params[0].name == "param2"

def test_clear_all_parameters():
    model = UmlProject()
    model.add_umlclass("temp")
    model.add_method("temp", "method1", "int", [("param1", "string")])

    model.clear_all_parameters("temp", "method1", "string")

    try:
        model.get_umlmethod("temp", "method1", "string")
    except Exception as e:
        assert e == errors.MethodOverloadNotExistsException()

    method = model.get_umlmethod("temp", "method1", "")

    assert len(method.params) == 0

def test_replace_all_parameters():
    model = UmlProject()
    model.add_umlclass("temp")
    model.add_method("temp", "method1", "int", [("param1", "string")])

    model.replace_all_parameters("temp", "method1", "string", [("param2", "int")])

    try:
        model.get_umlmethod("temp", "method1", "string")
    except Exception as e:
        assert e == errors.MethodOverloadNotExistsException()
    
    method = model.get_umlmethod("temp", "method1", "int")

    assert method is not None

def test_replace_all_parameters():
    model = UmlProject()
    model.add_umlclass("temp")
    model.add_method("temp", "method1", "int", [("param1", "string")])

    model.delete_parameter("temp", "method1", "string", "param1")

    try:
        model.get_umlmethod("temp", "method1", "string")
    except Exception as e:
        assert e == errors.MethodOverloadNotExistsException()
    
    method = model.get_umlmethod("temp", "method1", "")

    assert method is not None