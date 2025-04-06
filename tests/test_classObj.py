# Filename: test_classObj.py
# Authors: Kyle Kalbach, John Hershey, Juliana Vinluan, Evan Magill
# Creation Date: 02-06-2025, Last Edit Date: 04-05-2025
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
        test_class.add_field(test_field_name,"speed")
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidNameError"]
    assert "MaxSpeed" in test_class.class_fields

# Add an invalid Field
def test_add_field_invalid():
    """"""
    test_class = UmlClass("Car",{},{})
    test_field_name = "exit"

    try:
        test_class.add_field(test_field_name,"speed")
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidNameError"]
    assert len(test_class.class_fields) == 0

# Remove an existing Field
def test_remove_field_valid():
    """"""
    #change later to avoid direct assignment of fields
    test_field = UmlField("MaxSpeed","speed")
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
    test_field = UmlField("MaxSpeed","speed")
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
    test_field = UmlField("MaxSpeed","speed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})
    
    try:
        test_class.rename_field("MaxSpeed","MinSpeed")
    except Exception as e:
        pass
    assert "MinSpeed" in test_class.class_fields

# Rename an field to an invalid name
def test_rename_field_invalid():
    """"""
    test_field = UmlField("MaxSpeed","speed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})
    
    try:
        test_class.rename_field("MaxSpeed","relation")
    except Exception as e:
        assert e.get_num() == errors.error_list["InvalidNameError"]
    assert "MaxSpeed" in test_class.class_fields

# Rename a field to an existing field
def test_rename_field_existing():
    """"""
    test_field = UmlField("MaxSpeed","top_speed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})

    try:
        test_class.add_field("MinSpeed","slow_speed")
        test_class.rename_field("MaxSpeed","MinSpeed")
    except Exception as e:
        assert e.get_num() == errors.error_list["DuplicateFieldError"]
    assert "MaxSpeed" in test_class.class_fields
    assert "MinSpeed" in test_class.class_fields

# test adding method
def test_add_method_invalid_name():
    test_class = UmlClass("Car", {}, {})
    test_val = -1
    
    try:
        test_class.add_method("relation", "spaghetti", [])
    except Exception as e:
       test_val = e.get_num()
    finally:
        assert test_val == errors.error_list["InvalidNameError"]

def test_add_method_with_no_parameters():
    """"""
    test_class = UmlClass("Car", {}, {})
    chosen_return_type = "bool"
    test_method = UmlMethod("Drive", chosen_return_type, [])
    expected_overloadID = ""

    assert test_method.overloadID == expected_overloadID

    test_value = {"Drive": {expected_overloadID: test_method}}

    try:
        test_class.add_method("Drive", chosen_return_type, [])
    except Exception as e:
        assert False
    
    assert test_class.class_methods == test_value

def test_add_method_with_one_parameter():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_param_type = "CarPart"
    test_params = [("transmission", test_param_type)]
    test_return_type = "test_return_type"
    test_method = UmlMethod(test_method_name, test_return_type, [])
    test_method.add_parameters(test_params)

    expected_overloadID = test_param_type
    test_value = {test_method_name: {expected_overloadID: test_method}}

    test_class.add_method(test_method_name, test_return_type, test_params)
    
    assert test_class.class_methods == test_value

def test_add_method_with_multiple_parameter():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_method_return_type = "bool"
    test_params = [("transmission", "CarPart"), ("speed_limit", "Speed")]
    test_method = UmlMethod(test_method_name, test_method_return_type, [])
    test_method.add_parameters(test_params)
    test_value = {test_method_name: {"CarPart Speed": test_method}}

    test_class.add_method(test_method_name, test_method_return_type, test_params)
    
    assert test_class.class_methods == test_value

# test adding method overload
def test_adding_method_overload_valid():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_method_return_type = "bool"
    test_params = [("transmission", "CarPart")]
    test_method = UmlMethod(test_method_name, test_method_return_type, [])
    test_method_overload = UmlMethod(test_method_name, test_method_return_type, [])
    test_method_overload.add_parameters(test_params)
    test_value = {test_method_name: {"": test_method, "CarPart":test_method_overload}}

    try:
        test_class.add_method(test_method_name, test_method_return_type, [])
        test_class.add_method(test_method_name, test_method_return_type, test_params)
    except Exception as e:
        assert False
    
    assert test_class.class_methods == test_value

def test_adding_method_overload_invalid():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_method_return_type = "bool"
    test_params = [("transmission", "CarPart")]
    test_val = -1

    try:
        test_class.add_method(test_method_name, test_method_return_type, [])
        test_class.add_method(test_method_name, test_method_return_type, test_params)
        test_class.add_method(test_method_name, test_method_return_type, test_params)
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
    test_method_return_type = "bool"
    test_params = [("transmission", "CarPart")]
    test_method = UmlMethod(test_method_rename, test_method_return_type, [])
    test_method.add_parameters(test_params)
    test_val = {test_method_rename: {"CarPart": test_method}}

    test_class.add_method(test_method_name, test_method_return_type, test_params)
    test_class.rename_method(test_method_name, "CarPart", test_method_rename)

    assert test_class.class_methods == test_val

def test_rename_method_invalid():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_method_rename = "relation"
    test_method_return_type = "bool"
    test_params = [("transmission", "CarPart")]
    test_method = UmlMethod(test_method_name, test_method_return_type, [])
    test_method.add_parameters(test_params)
    test_val_error = -1
    test_val_methods = {test_method_name: {"CarPart": test_method}}

    test_class.add_method(test_method_name, test_method_return_type, test_params)
    try:
        test_class.rename_method(test_method_name, "CarPart", test_method_rename)
    except Exception as e:
        test_val_error = e.get_num()
    finally:
        assert test_class.class_methods == test_val_methods
        assert test_val_error == errors.error_list["InvalidNameError"]

def test_rename_method_overload_valid():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_method_rename = "Park"
    test_method_return_type = "bool"
    test_params = [("transmission", "CarPart")]
    test_method = UmlMethod(test_method_name, test_method_return_type, [])
    test_method.add_parameters(test_params)
    test_method_overload = UmlMethod(test_method_name, test_method_return_type, [])
    test_val_methods = {test_method_name: {"": test_method_overload, "CarPart": test_method}}

    # add method Drive and Park
    test_class.add_method(test_method_name, test_method_return_type, test_params)
    test_class.add_method(test_method_rename, test_method_return_type, [])

    # Rename method Park so it becomes an overload of method Drive
    test_class.rename_method(test_method_rename, "", test_method_name)

    assert test_class.class_methods == test_val_methods

def test_rename_method_overload_invalid():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_method_rename = "Park"
    test_method_return_type = "bool"
    test_params = [("transmission", "CarPart")]
    test_method = UmlMethod(test_method_name, test_method_return_type, [])
    test_method.add_parameters(test_params)
    test_method_overload = UmlMethod(test_method_rename, test_method_return_type, [])
    test_method_overload.add_parameters(test_params)
    test_val_methods = {
        test_method_name: {"CarPart": test_method},
        test_method_rename: {"CarPart": test_method_overload}
    }
    test_val_error = -1

    # add method Drive and Park
    test_class.add_method(test_method_name, test_method_return_type, test_params)
    test_class.add_method(test_method_rename, test_method_return_type, test_params)

    # Rename method Park so it becomes an overload of method Drive
    try:
        test_class.rename_method(test_method_rename, "CarPart", test_method_name)
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
    test_method_return_type = "bool"
    test_params = [("transmission", "CarPart")]
    test_method = UmlMethod(test_method_name, test_method_return_type, [])
    test_method.add_parameters(test_params)
    test_val_methods = {}

    test_class.add_method(test_method_name, test_method_return_type, test_params)
    test_class.remove_method(test_method_name, "CarPart")

    assert test_class.class_methods == test_val_methods

def test_remove_method_invalid():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_method_invalid_name = "Park"
    test_method_return_type = "bool"
    test_params = [("transmission", "CarPart")]
    test_method = UmlMethod(test_method_name, test_method_return_type, [])
    test_method.add_parameters(test_params)
    test_val_methods = {test_method_name: {"CarPart": test_method}}
    test_val_error = -1

    test_class.add_method(test_method_name, test_method_return_type, test_params)

    # Invalid method name case
    try:
        test_class.remove_method(test_method_invalid_name, "CarPart")
    except Exception as e:
        test_val_error = e.get_num()
    finally:
        assert test_class.class_methods == test_val_methods
        assert test_val_error == errors.error_list["MethodNameNotExistsError"]

def test_remove_method_overload_invalid():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_method_return_type = "bool"
    test_params = [("transmission", "CarPart")]
    test_method = UmlMethod(test_method_name, test_method_return_type, [])
    test_method.add_parameters(test_params)
    test_val_methods = {test_method_name: {"CarPart": test_method}}
    test_val_error = -1

    test_class.add_method(test_method_name, test_method_return_type, test_params)
    # Invalid overloadID case
    try:
        test_class.remove_method(test_method_name, "")
    except Exception as e:
        test_val_error = e.get_num()
    finally:
        assert test_class.class_methods == test_val_methods
        assert test_val_error == errors.error_list["MethodOverloadNotExistsError"]

# test removing all methods
def test_remove_method_all():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_method_return_type = "bool"
    test_params = [("transmission", "CarPart")]
    test_method = UmlMethod(test_method_name, test_method_return_type, [])
    test_method.add_parameters(test_params)
    test_val_methods = {}
    
    test_class.add_method(test_method_name, test_method_return_type, test_params)

    test_class.remove_all_methods()

    assert test_class.class_methods == test_val_methods

# test removing all method overloads
def test_remove_method_all_overloads():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_method_return_type = "bool"
    test_params = [("transmission", "CarPart")]
    test_method = UmlMethod(test_method_name, test_method_return_type, [])
    test_method.add_parameters(test_params)
    test_val_methods = {}
    
    test_class.add_method(test_method_name, test_method_return_type, test_params)
    test_class.add_method(test_method_name, test_method_return_type, [])

    test_class.remove_all_overloads(test_method_name)

    assert test_class.class_methods == test_val_methods

# TODO - Unit tests replace all method parameters

# test replacing all method parameters
def test_replace_all_method_parameters():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_method_return_type = "bool"
    test_params = [("transmission", "CarPart")]
    test_method = UmlMethod(test_method_name, test_method_return_type, [])
    test_method.add_parameters(test_params)
    test_val_methods = {test_method_name: {"CarPart": test_method}}

    test_class.add_method(test_method_name, test_method_return_type, [])
    test_class.replace_all_parameters(test_params)

    assert test_class.class_methods == test_val_methods

# TODO - Unit tests clear all method parameters
