# Filename: unit_tests.py
# Authors: Kyle Kalbach, John Hershey
# Creation Date: 02-06-2025, Last Edit Date: 02-08-2025
# Description: Unit Tests for uml.py
import pytest
import os
import sys
import logging
# use below to add directory to system path
# sys.path.append(os.path.abspath(os.path.join('..', '2025sp-420-BarkingSnakes')))
# adds the repo directory to sys.path
# os.path.abspath is the route to the class directory
#rootDir = '2025sp-420-BarkingSnakes'
#if os.path.abspath('.') not in sys.path:
    #sys.path.append(os.path.abspath('.'))
# errors can be imported once the path has been added
#import src.errors as errors
from src import errors
#Add a valid class

#Add an invalid class 
def testInvalidName():
    x = None
    #checks
    try:
        errors.validName("class")
    except Exception as e:
        logging.log(0,f"error name is {e.name}, num={e.errorNum}")
    assert x == errors.errorList["InvalidNameError"]

    
#Add an existing class

#Delete an existing class

#Delete a non-existing class
#using empty class
def testDeleteEmpty():
    x = None
    try:
        errors.noClass(None)
    except Exception as e:
        logging.log(0,f"error name is {e.name}, num={e.errorNum}")
        x=e
    assert x.errorNum == errors.errorList["NullObjectError"]
#Delete an invalid class name

#Rename an existing class to a valid class name

#Rename an existing class to an invalid class name

#Rename Rename a class that does not exist
