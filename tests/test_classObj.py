# Filename: unit_tests.py
# Authors: Kyle Kalbach, John Hershey
# Creation Date: 02-06-2025, Last Edit Date: 02-08-2025
# Description: Unit Tests for uml.py
import os
import sys
import logging
from src.umlclass import UmlClass
from src import errors
# from src import errors

# use below to add directory to system path
# sys.path.append(os.path.abspath(os.path.join('..', '2025sp-420-BarkingSnakes')))
# adds the repo directory to sys.path
# os.path.abspath is the route to the class directory
rootDir = '2025sp-420-BarkingSnakes'
if os.path.abspath('.') not in sys.path:
    sys.path.append(os.path.abspath('.'))
# errors can be imported once the path has been added

# Rename an existing class to a valid class name
def test_rename_existing_class():
    """"""
    test_class = UmlClass()
    test_class.class_name = "OriginalName"
    try:
        test_class.rename_umlclass("NewName")
    except:
        pass

    assert test_class.class_name == "NewName"
        
# Rename an existing class to an invalid class name
def test_rename_class_invalid():
    """"""
    test_class = UmlClass()
    test_class.class_name = "OriginalName"
    try:
        test_class.rename_umlclass(test_class,"class")
    except Exception as e:
        assert e == errors.errorList["InvalidNameError"]
        
    assert test_class.class_name == "OriginalName"    
    
    
# Rename Rename a class that does not exist

# Add a valid Attribute

# Add an invalid Attribute

# Remove an existing Attribute

# Remove a nonexisting Attribute




# This code needs to move to the UML project Test

# Add a valid class

# Add an invalid class 
# def testInvalidName():
#     x = None
#     #checks
#     try:
#         errors.validName("class")
#     except Exception as e:
#         logging.log(0,f"error name is {e.name}, num={e.errorNum}")
#     assert x == errors.errorList["InvalidNameError"]

# Add an existing class

# Delete an existing class

# Delete a non-existing class
# using empty class
# def testDeleteEmpty():
#     x = None
#     try:
#         errors.noClass(None)
#     except Exception as e:
#         logging.log(0,f"error name is {e.name}, num={e.errorNum}")
#         x=e
#     assert x.errorNum == errors.errorList["NullObjectError"]

# Delete an invalid class name
