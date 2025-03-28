# Filename: test_fieldObj.py
# Authors: Kyle Kalbach, John Hershey, Juliana Vinluan
# Creation Date: 2025-02-12, Last Edit Date: 2025-02-24
# Description: Unit Tests for field.py
import os
import sys
import logging
from src.umlclass import UmlClass
from src.umlfield import UmlField
from src import errors

# use below to add directory to system path
# sys.path.append(os.path.abspath(os.path.join('..', '2025sp-420-BarkingSnakes')))
# adds the repo directory to sys.path
# os.path.abspath is the route to the class directory
root_dir = '2025sp-420-BarkingSnakes'
if os.path.abspath('.') not in sys.path:
    sys.path.append(os.path.abspath('.'))

# Rename a field
def test_rename_field_valid():
    """"""
    test_field = UmlField("OriginalName","speed")
    assert test_field.name == "OriginalName"

    try:
        test_field.rename_field("NewName")
    except Exception as e:
        assert e.get_num() == errors.error_list["InvalidNameError"]
    assert test_field.name == "NewName"

# Rename a field
def test_field_valid():
    """"""
    test_name = "speed"
    test_type = "int"
    test_class = UmlClass("Car")

    try:
        test_class.add_field(test_name, test_type)
    except Exception as e:
        assert e.get_num() == errors.error_list["InvalidNameError"]
    assert test_class.fields[test_name].type == test_type