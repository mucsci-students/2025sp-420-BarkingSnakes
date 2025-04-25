# Filename: test_fieldObj.py
# Authors: Kyle Kalbach, John Hershey, Juliana Vinluan
# Creation Date: 2025-02-12, Last Edit Date: 03-28-2025
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
        assert e == errors.InvalidNameException()
    assert test_field.name == "NewName"
