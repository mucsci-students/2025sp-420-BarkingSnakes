# Filename: test_fieldObj.py
# Authors: Kyle Kalbach, John Hershey, Juliana Vinluan
# Creation Date: 2025-02-12, Last Edit Date: 2025-04-27
# Description: Unit Tests for field.py
import os
from src.umlclass import UmlClass
from src.umlfield import UmlField
from src import errors

# Rename a field
def test_rename_field_valid():
    """tests when new name is valid"""
    test_field = UmlField("OriginalName","speed")
    assert test_field.name == "OriginalName"

    try:
        test_field.rename_field("NewName")
    except Exception as e:
        assert e == errors.InvalidNameException()
    assert test_field.name == "NewName"
    
def test_rename_field_invalid():
    """tests when new name is invalid"""
    test_field = UmlField("OriginalName","speed")
    assert test_field.name == "OriginalName"

    try:
        test_field.rename_field("9th")
        assert False
    except Exception as e:
        assert e == errors.InvalidNameException()
    assert test_field.name == "OriginalName"
    
# change type
def test_change_field_type_valid():
    """tests when new type is valid"""
    test_field = UmlField("Name","speed")
    assert test_field.type == "speed"
    try:
        test_field.change_type("time")
    except Exception as e:
        assert e == None
    assert test_field.type == "time"
    
def test_change_field_type_invalid():
    """tests when new type is valid"""
    test_field = UmlField("Name","speed")
    assert test_field.type == "speed"

    try:
        test_field.change_type("9th")
        assert False
    except Exception as e:
        assert e == errors.InvalidNameException()
    assert test_field.type == "speed"
    
# to dict
def test_to_dict():
    """tests to dict method"""
    test_field = UmlField("Name","speed")
    try:
        fdict = test_field.to_dict()
        assert fdict == {"name": "Name", "type": "speed"}
    except Exception as e:
        assert e == None

