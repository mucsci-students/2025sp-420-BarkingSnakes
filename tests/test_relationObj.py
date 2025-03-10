# Filename: test_fieldObj.py
# Authors: John Hershey
# Creation Date: 2025-03-9, Last Edit Date: 2025-03-9
# Description: Unit Tests for umlrelationship.py
import os
import sys
from src.umlclass import UmlClass
from src.umlrelationship import UmlRelationship
from src.umlmodel import UmlProject
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
def test_add_relation_no_classes():
    """tests that an error is raised if classes in relation don't exist"""
    var = 1
    try:
        proj = UmlProject()
        proj.add_relationship("temp", "temp2", 0)
    except Exception as e:
        var = None
        assert e == errors.NoSuchObjectException()
    assert not var



    
    