# Filename: test_attributeObj.py
# Authors: Kyle Kalbach, John Hershey
# Creation Date: 02-12-2025, Last Edit Date: 02-12-2025
# Description: Unit Tests for attribute.py
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

# Rename an attribute
def test_rename_attribute_valid():
    """"""
    test_attribute = Attribute("OriginalName")
    assert test_attribute.name == "OriginalName"

    try:
        test_attribute.rename_attr("NewName")
    except Exception as e:
        assert e.get_num() == errors.error_list["InvalidNameError"]
    assert test_attribute.name == "NewName"
