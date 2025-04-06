# Filename: test_paramObj.py
# Authors: Kyle Kalbach, John Hershey, Juliana Vinluan, Evan Magill
# Creation Date: 06-04-2025, Last Edit Date: 06-04-2025
# Description: Unit Tests for umlclass.py
import os
import sys
import logging

from src.umlclass import UmlClass
from src.umlfield import UmlField
from src.umlmethod import UmlMethod
from src.umlparameter import UmlParameter
from src import errors

def test_rename_param():
    test_param = UmlParameter("MaxSpeed","mph")

    test_param.rename_parameter("MinSpeed")

    assert test_param.name == "MinSpeed"

def test_change_parameter_type():
    test_param = UmlParameter("MaxSpeed","mph")

    test_param.change_parameter_type("kph")

    assert test_param.umltype == "kph"

def test_to_dict():
    test_param = UmlParameter("MaxSpeed","mph")

    test_dict = test_param.to_dict()
    
    assert test_dict == {'name':'MaxSpeed','type':'mph'}
