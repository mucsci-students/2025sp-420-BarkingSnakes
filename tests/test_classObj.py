# Filename: unit_tests.py
# Authors: Kyle Kalbach, John Hershey
# Creation Date: 02-06-2025, Last Edit Date: 02-12-2025
# Description: Unit Tests for umlclass.py
import os
import sys
import logging
from src.umlclass import UmlClass
from src.attribute import Attribute
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
    
# Rename a class that does not exist

# Rename a class to an existing class name 

# Add a valid Attribute
def test_add_attribute_valid():
    """"""
    test_class = UmlClass("Car",{})
    test_attribute = Attribute("MaxSpeed")

    try:
        test_class.add_attribute(test_attribute)
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidNameError"]
    assert "MaxSpeed" in test_class.class_attributes

# Add an invalid Attribute
def test_add_attribute_invalid():
    """"""
    test_class = UmlClass("Car",{})
    test_attribute = Attribute("exit")

    try:
        test_class.add_attribute(test_attribute)
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidNameError"]
    assert len(test_class.class_attributes) == 0

# Remove an existing Attribute
def test_remove_attribute_valid():
    """"""
    test_attribute = Attribute("MaxSpeed")
    test_class = UmlClass("Car",{"MaxSpeed":test_attribute})

    assert len(test_class.class_attributes) == 1
    
    try:
        test_class.remove_attribute(test_attribute.name)
        
    except Exception as e:
       assert e.get_num() == errors.error_list["NoSuchObjectError"]
    assert len(test_class.class_attributes) == 0

# Remove a nonexisting Attribute
def test_remove_attribute_not_found():
    """"""
    test_attribute = Attribute("MaxSpeed")
    test_class = UmlClass("Car",{"MaxSpeed":test_attribute})

    assert len(test_class.class_attributes) == 1
    
    try:
        test_class.remove_attribute("MinSpeed")
        
    except Exception as e:
       assert e.get_num() == errors.error_list["NoSuchObjectError"]
    assert len(test_class.class_attributes) == 1

# Rename an attribute
def test_rename_attribute_valid():
    """"""
    test_attribute = Attribute("MaxSpeed")
    test_class = UmlClass("Car",{"MaxSpeed":test_attribute})
    
    try:
        test_class.rename_attribute("MaxSpeed","MinSpeed")
    except Exception as e:
        pass
    assert "MinSpeed" in test_class.class_attributes

# Rename an attribute to an invalid name
def test_rename_attribute_invalid():
    """"""
    test_attribute = Attribute("MaxSpeed")
    test_class = UmlClass("Car",{"MaxSpeed":test_attribute})
    
    try:
        test_class.rename_attribute("MaxSpeed","relation")
    except Exception as e:
        assert e.get_num() == errors.error_list["InvalidNameError"]
    assert "MaxSpeed" in test_class.class_attributes

# Rename an attribute to an existing attribute
def test_rename_attribute_existing():
    """"""
    test_attribute = Attribute("MaxSpeed")
    test_class = UmlClass("Car",{"MaxSpeed":test_attribute})

    try:
        test_class.rename_attribute("MaxSpeed","MaxSpeed")
    except Exception as e:
        assert e.get_num() == errors.error_list["DuplicateAttributeError"]
    assert "MaxSpeed" in test_class.class_attributes

