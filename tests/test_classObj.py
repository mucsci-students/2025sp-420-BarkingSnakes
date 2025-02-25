# Filename: unit_tests.py
# Authors: Kyle Kalbach, John Hershey
# Creation Date: 02-06-2025, Last Edit Date: 02-12-2025
# Description: Unit Tests for umlclass.py
import os
import sys
import logging
from src.umlclass import UmlClass
from src.umlfield import UmlField
from src import errors
# from src import errors

# use below to add directory to system path
# sys.path.append(os.path.abspath(os.path.join('..', '2025sp-420-BarkingSnakes')))
# adds the repo directory to sys.path
# os.path.abspath is the route to the class directory
root_dir = '2025sp-420-BarkingSnakes'
if os.path.abspath('.') not in sys.path:
    sys.path.append(os.path.abspath('.'))
# errors can be imported once the path has been added

# Rename an existing class to a valid class name
def test_rename_existing_class():
    """"""
    test_class = UmlClass("OriginalName",{})
    try:
        test_class.rename_umlclass("NewName")
    except:
        pass

    assert test_class.class_name == "NewName"
        
# Rename an existing class to an invalid class name
def test_rename_class_invalid():
    """"""
    test_class = UmlClass("OriginalName",{})
    try:
        test_class.rename_umlclass("class")
    except Exception as e:
        assert e.get_num() == errors.error_list["InvalidNameError"]
    assert test_class.class_name == "OriginalName"    
    
# Add a valid Field
def test_add_field_valid():
    """"""
    test_class = UmlClass("Car",{})
    test_field_name = "MaxSpeed"

    try:
        test_class.add_field(test_field_name)
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidNameError"]
    assert "MaxSpeed" in test_class.class_fields

# Add an invalid Field
def test_add_field_invalid():
    """"""
    test_class = UmlClass("Car",{})
    test_field_name = "exit"

    try:
        test_class.add_field(test_field_name)
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidNameError"]
    assert len(test_class.class_fields) == 0

# Remove an existing Field
def test_remove_field_valid():
    """"""
    #change later to avoid direct assignment of fields
    test_field = UmlField("MaxSpeed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field})

    assert len(test_class.class_fields) == 1
    
    try:
        test_class.remove_field(test_field.name)
        
    except Exception as e:
       assert e.get_num() == errors.error_list["NoSuchObjectError"]
    assert len(test_class.class_fields) == 0

# Remove a nonexisting Field
def test_remove_field_not_found():
    """"""
    test_field = UmlField("MaxSpeed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field})

    assert len(test_class.class_fields) == 1
    
    try:
        test_class.remove_field("MinSpeed")
        
    except Exception as e:
       assert e.get_num() == errors.error_list["NoSuchObjectError"]
    assert len(test_class.class_fields) == 1

# Rename an field
def test_rename_field_valid():
    """"""
    test_field = UmlField("MaxSpeed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field})
    
    try:
        test_class.rename_field("MaxSpeed","MinSpeed")
    except Exception as e:
        pass
    assert "MinSpeed" in test_class.class_fields

# Rename an field to an invalid name
def test_rename_field_invalid():
    """"""
    test_field = UmlField("MaxSpeed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field})
    
    try:
        test_class.rename_field("MaxSpeed","relation")
    except Exception as e:
        assert e.get_num() == errors.error_list["InvalidNameError"]
    assert "MaxSpeed" in test_class.class_fields

# Rename a field to an existing field
def test_rename_field_existing():
    """"""
    test_field = UmlField("MaxSpeed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field})

    try:
        test_class.rename_field("MaxSpeed","MaxSpeed")
    except Exception as e:
        assert e.get_num() == errors.error_list["DuplicateFieldError"]
    assert "MaxSpeed" in test_class.class_fields

