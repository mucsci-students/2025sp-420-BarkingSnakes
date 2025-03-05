# Filename: unit_tests.py
# Authors: Kyle Kalbach, John Hershey
# Creation Date: 02-06-2025, Last Edit Date: 02-12-2025
# Description: Unit Tests for umlclass.py
import os
import sys
import logging

from src.umlclass import UmlClass
from src.umlfield import UmlField
from src.umlmethod import UmlMethod
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
    test_class = UmlClass("OriginalName",{},{})
    try:
        test_class.rename_umlclass("NewName")
    except:
        pass

    assert test_class.class_name == "NewName"
        
# Rename an existing class to an invalid class name
def test_rename_class_invalid():
    """"""
    test_class = UmlClass("OriginalName",{},{})
    try:
        test_class.rename_umlclass("class")
    except Exception as e:
        assert e.get_num() == errors.error_list["InvalidNameError"]
    assert test_class.class_name == "OriginalName"    
    
# Add a valid Field
def test_add_field_valid():
    """"""
    test_class = UmlClass("Car",{},{})
    test_field_name = "MaxSpeed"

    try:
        test_class.add_field(test_field_name)
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidNameError"]
    assert "MaxSpeed" in test_class.class_fields

# Add an invalid Field
def test_add_field_invalid():
    """"""
    test_class = UmlClass("Car",{},{})
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
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})

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
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})

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
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})
    
    try:
        test_class.rename_field("MaxSpeed","MinSpeed")
    except Exception as e:
        pass
    assert "MinSpeed" in test_class.class_fields

# Rename an field to an invalid name
def test_rename_field_invalid():
    """"""
    test_field = UmlField("MaxSpeed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})
    
    try:
        test_class.rename_field("MaxSpeed","relation")
    except Exception as e:
        assert e.get_num() == errors.error_list["InvalidNameError"]
    assert "MaxSpeed" in test_class.class_fields

# Rename a field to an existing field
def test_rename_field_existing():
    """"""
    test_field = UmlField("MaxSpeed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})

    try:
        test_class.rename_field("MaxSpeed","MaxSpeed")
    except Exception as e:
        assert e.get_num() == errors.error_list["DuplicateFieldError"]
    assert "MaxSpeed" in test_class.class_fields

# test adding method
def test_add_method_invalid_name():
    test_class = UmlClass("Car", {}, {})
    test_val = -1
    
    try:
        test_class.add_method("relation", [])
    except Exception as e:
       test_val = e.get_num()
    finally:
        assert test_val == errors.error_list["InvalidNameError"]

def test_add_method_with_no_parameters():
    """"""
    test_class = UmlClass("Car", {}, {})
    test_method = UmlMethod("Drive", {})
    test_value = {"Drive": {0: test_method}}

    try:
        test_class.add_method("Drive", [])
    except Exception as e:
        assert False
    
    assert test_class.class_methods == test_value

def test_add_method_with_one_parameter():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_params = ["transmission"]
    test_method = UmlMethod(test_method_name, {})
    test_method.add_parameters(test_params)

    test_value = {test_method_name: {1: test_method}}

    test_class.add_method(test_method_name, test_params)
    
    assert test_class.class_methods == test_value

def test_add_method_with_multiple_parameter():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_params = ["transmission", "speed_limit"]
    test_method = UmlMethod(test_method_name, {})
    test_method.add_parameters(test_params)
    test_value = {test_method_name: {2: test_method}}

    test_class.add_method(test_method_name, test_params)
    
    assert test_class.class_methods == test_value

# test adding method overload
def test_adding_method_overload_valid():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_params = ["transmission"]
    test_method = UmlMethod(test_method_name, {})
    test_method_overload = UmlMethod(test_method_name, {})
    test_method_overload.add_parameters(test_params)
    test_value = {test_method_name: {0: test_method, 1:test_method_overload}}

    try:
        test_class.add_method(test_method_name, [])
        test_class.add_method(test_method_name, test_params)
    except Exception as e:
        assert False
    
    assert test_class.class_methods == test_value

def test_adding_method_overload_valid():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_params = ["transmission"]
    test_method = UmlMethod(test_method_name, {})
    test_method_overload = UmlMethod(test_method_name, {})
    test_method_overload.add_parameters(test_params)
    test_value = {test_method_name: {0: test_method, 1:test_method_overload}}

    try:
        test_class.add_method(test_method_name, [])
        test_class.add_method(test_method_name, test_params)
    except Exception as e:
        assert False
    
    assert test_class.class_methods == test_value

def test_adding_method_overload_invalid():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_params = ["transmission"]
    test_val = -1

    try:
        test_class.add_method(test_method_name, [])
        test_class.add_method(test_method_name, test_params)
        test_class.add_method(test_method_name, test_params)
    except Exception as e:
        test_val = e.get_num()
    finally:
        assert test_val == errors.error_list["DuplicateMethodOverloadError"]

# test renaming method
#   - produces overload
#     - invalid case
#     - valid case
#   - removes overload
#     - invalid case
#     - valid case
#   - transfers overload
#     - invalid case
#     - valid case
#   - valid name case
#   - invalid name case
def test_rename_method_valid():
    """"""
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_method_rename = "Park"
    test_params = ["transmission"]
    test_method = UmlMethod(test_method_rename, {})
    test_method.add_parameters(test_params)
    test_val = {test_method_rename: {1: test_method}}

    test_class.add_method(test_method_name, test_params)
    test_class.rename_method(test_method_name, len(test_params), test_method_rename)

    assert test_class.class_methods == test_val

def test_rename_method_invalid():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_method_rename = "relation"
    test_params = ["transmission"]
    test_method = UmlMethod(test_method_name, {})
    test_method.add_parameters(test_params)
    test_val_error = -1
    test_val_methods = {test_method_name: {1: test_method}}

    test_class.add_method(test_method_name, test_params)
    try:
        test_class.rename_method(test_method_name, len(test_params), test_method_rename)
    except Exception as e:
        test_val_error = e.get_num()
    finally:
        assert test_class.class_methods == test_val_methods
        assert test_val_error == errors.error_list["InvalidNameError"]

def test_rename_method_overload_valid():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_method_rename = "Park"
    test_params = ["transmission"]
    test_method = UmlMethod(test_method_name, {})
    test_method.add_parameters(test_params)
    test_method_overload = UmlMethod(test_method_name, {})
    test_val_methods = {test_method_name: {0: test_method_overload, 1: test_method}}

    # add method Drive and Park
    test_class.add_method(test_method_name, test_params)
    test_class.add_method(test_method_rename, [])

    # Rename method Park so it becomes an overload of method Drive
    test_class.rename_method(test_method_rename, 0, test_method_name)

    assert test_class.class_methods == test_val_methods

def test_rename_method_overload_invalid():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_method_rename = "Park"
    test_params = ["transmission"]
    test_method = UmlMethod(test_method_name, {})
    test_method.add_parameters(test_params)
    test_method_overload = UmlMethod(test_method_rename, {})
    test_method_overload.add_parameters(test_params)
    test_val_methods = {
        test_method_name: {1: test_method},
        test_method_rename: {1: test_method_overload}
    }
    test_val_error = -1

    # add method Drive and Park
    test_class.add_method(test_method_name, test_params)
    test_class.add_method(test_method_rename, test_params)

    # Rename method Park so it becomes an overload of method Drive
    try:
        test_class.rename_method(test_method_rename, 1, test_method_name)
    except Exception as e:
        test_val_error = e.get_num()
    finally:
        assert test_class.class_methods == test_val_methods
        assert test_val_error == errors.error_list['DuplicateMethodOverloadError']

# test removing method
#   - invalid name case
#   - valid case
#     - one overload complete removes method from top tier dict
#   - invalid arity case
def test_remove_method_valid():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_params = ["transmission"]
    test_method = UmlMethod(test_method_name, {})
    test_method.add_parameters(test_params)
    test_val_methods = {}

    test_class.add_method(test_method_name, test_params)
    test_class.remove_method(test_method_name, len(test_params))

    assert test_class.class_methods == test_val_methods

def test_remove_method_invalid():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_method_invalid_name = "Park"
    test_params = ["transmission"]
    test_method = UmlMethod(test_method_name, {})
    test_method.add_parameters(test_params)
    test_val_methods = {test_method_name: {1: test_method}}
    test_val_error = -1

    test_class.add_method(test_method_name, test_params)

    # Invalid method name case
    try:
        test_class.remove_method(test_method_invalid_name, len(test_params))
    except Exception as e:
        test_val_error = e.get_num()
    finally:
        assert test_class.class_methods == test_val_methods
        assert test_val_error == errors.error_list["MethodNameNotExistsError"]

def test_remove_method_overload_invalid():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_params = ["transmission"]
    test_method = UmlMethod(test_method_name, {})
    test_method.add_parameters(test_params)
    test_val_methods = {test_method_name: {1: test_method}}
    test_val_error = -1

    test_class.add_method(test_method_name, test_params)
    # Invalid arity case
    try:
        test_class.remove_method(test_method_name, 0)
    except Exception as e:
        test_val_error = e.get_num()
    finally:
        assert test_class.class_methods == test_val_methods
        assert test_val_error == errors.error_list["MethodOverloadNotExistsError"]

# test removing all methods
def test_remove_method_all():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_params = ["transmission"]
    test_method = UmlMethod(test_method_name, {})
    test_method.add_parameters(test_params)
    test_val_methods = {}
    
    test_class.add_method(test_method_name, test_params)

    test_class.remove_all_methods()

    assert test_class.class_methods == test_val_methods

# test removing all method overloads
def test_remove_method_all_overloads():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_params = ["transmission"]
    test_method = UmlMethod(test_method_name, {})
    test_method.add_parameters(test_params)
    test_val_methods = {}
    
    test_class.add_method(test_method_name, test_params)
    test_class.add_method(test_method_name, [])

    test_class.remove_all_overloads(test_method_name)

    assert test_class.class_methods == test_val_methods