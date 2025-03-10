# Filename: test_fieldObj.py
# Authors: John Hershey
# Creation Date: 2025-03-9, Last Edit Date: 2025-03-9
# Description: Unit Tests for umlrelationship.py
import os
import sys
from src.umlclass import UmlClass
from src.umlrelationship import UmlRelationship
from src import errors

def test_circular_relation():
    """tests that a circular relationship doesn't raise an error"""
    var = None
    try:
        class1= UmlClass("name")
        relation = UmlRelationship(0,class1, class1)
    except Exception as e:
        var = 1
        assert e == None
    assert not var
    
    