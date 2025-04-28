# Filename: test_classObj.py
# Authors: Kyle Kalbach, John Hershey, Juliana Vinluan, Evan Magill
# Creation Date: 02-06-2025, Last Edit Date: 04-18-2025
# Description: Unit Tests for umlclass.py

from src.umlclass import UmlClass
from src.umlfield import UmlField
from src.umlmethod import UmlMethod
from src.umlparameter import UmlParameter
from src import errors

# Rename an existing class to a valid class name
def test_rename_existing_class():
    """"""
    test_class = UmlClass("OriginalName",{},{})
    try:
        test_class.rename_umlclass("NewName")
    except:
        pass

    assert test_class.class_name == "NewName"
        
# Rename an existing class to a no longer invalid class name
def test_rename_class_invalid():
    """make sure naming a class with a keyword does not raise an error"""
    test_class = UmlClass("OriginalName",{},{})
    try:
        test_class.rename_umlclass("class")
    except Exception as e:
        assert e == None
    assert test_class.class_name == "class"    
    
# Add a valid Field
def test_add_field_valid():
    """"""
    test_class = UmlClass("Car",{},{})
    test_field_name = "MaxSpeed"

    try:
        test_class.add_field(test_field_name,"speed")
    except Exception as e:
       assert e == None
    assert "MaxSpeed" in test_class.class_fields

# Add an invalid Field
def test_add_field_invalid():
    """test that a python keyword does not raise an error"""
    test_class = UmlClass("Car",{},{})
    test_field_name = "exit"

    try:
        test_class.add_field(test_field_name,"speed")
    except Exception as e:
       assert e == None
    assert len(test_class.class_fields) == 1

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
       assert e == errors.NoSuchObjectException()
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
       assert e == errors.NoSuchObjectException()
    assert len(test_class.class_fields) == 1

## renaming fields
def test_rename_field_valid():
    """test renaming a field normally"""
    test_field = UmlField("MaxSpeed","speed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})
    
    try:
        test_class.rename_field("MaxSpeed","MinSpeed")
    except Exception as e:
        pass
    assert "MinSpeed" in test_class.class_fields

def test_rename_field_not_invalid():
    """make sure that naming a field to a keyword does not raise an error"""
    test_field = UmlField("MaxSpeed","speed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})
    
    try:
        test_class.rename_field("MaxSpeed","relation")
    except Exception as e:
        assert e == None
    assert "MaxSpeed" not in test_class.class_fields
    assert "relation" in test_class.class_fields
    
def test_rename_field_invalid():
    """make sure that naming a field to a number does raise an error"""
    test_field = UmlField("MaxSpeed","speed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})
    
    try:
        test_class.rename_field("MaxSpeed","9th")
        assert False
    except Exception as e:
        assert e == errors.InvalidNameException()
    assert "MaxSpeed" in test_class.class_fields
    assert "9th" not in test_class.class_fields

def test_rename_field_existing():
    """test that renaming a field to an existing field errors"""
    test_field = UmlField("MaxSpeed","top_speed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})

    try:
        test_class.add_field("MinSpeed","slow_speed")
        test_class.rename_field("MaxSpeed","MinSpeed")
    except Exception as e:
        assert e == errors.DuplicateFieldException()
    assert "MaxSpeed" in test_class.class_fields
    assert "MinSpeed" in test_class.class_fields
    
def test_rename_field_not_existing():
    """make sure that renaming a nonexistent field errors"""
    test_field = UmlField("MaxSpeed","speed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})
    
    try:
        test_class.rename_field("MinSpeed","name")
        assert False
    except Exception as e:
        assert e == errors.NoSuchObjectException()
    assert "MaxSpeed" in test_class.class_fields
    assert "name" not in test_class.class_fields
    
## change type method tests
def test_change_field_type_valid():
    """test that changing a field type works"""
    test_field = UmlField("MaxSpeed","top_speed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})

    try:
        test_class.add_field("MinSpeed","slow_speed")
        test_class.change_field_type("MinSpeed","mph")
    except Exception as e:
        assert e == None
    assert "MinSpeed" in test_class.class_fields
    assert "mph" == test_class.class_fields["MinSpeed"].type
    
def test_change_field_type_no_field():
    """test that changing a field type when the field doesn't exist errors"""
    test_class = UmlClass("Car",{},{})
    try:
        test_class.add_field("MinSpeed","slow_speed")
        test_class.change_field_type("MaxSpeed","mph")
        assert False
    except Exception as e:
        assert e == errors.NoSuchObjectException()
    assert "MaxSpeed" not in test_class.class_fields
    assert "MinSpeed" in test_class.class_fields
    assert "slow_speed" == test_class.class_fields["MinSpeed"].type
    
def test_change_field_type_invalid_name():
    """test that changing a field type errors if the type is invalid"""
    test_field = UmlField("MaxSpeed","top_speed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})

    try:
        test_class.add_field("MinSpeed","slow_speed")
        test_class.change_field_type("MinSpeed","9th")
        assert False
    except Exception as e:
        assert e == errors.InvalidNameException()
    assert "MinSpeed" in test_class.class_fields
    assert "slow_speed" == test_class.class_fields["MinSpeed"].type

## test adding method
def test_add_method_not_invalid_name():
    """tests that a keyword doesn't raise an error"""
    test_class = UmlClass("Car", {}, {})
    try:
        test_class.add_method("relation1", "spaghetti", [])
    except Exception as e:
        assert e == None
    assert "relation1" in test_class.class_methods
    
    
    # test adding method
def test_add_method_invalid_name():
    """"""
    test_class = UmlClass("Car", {}, {})
    try:
        test_class.add_method("3the", "spaghetti", [])
        assert False
    except Exception as e:
       assert e == errors.InvalidNameException()

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
        assert e == None
    
    assert test_class.class_methods == test_value
    
### umlmethod class tests
def test_add_existing_parameter():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_param_type = "CarPart"
    test_param_name = "transmission"
    test_return_type = "test_return_type"
    test_method = UmlMethod(test_method_name, test_return_type, [])
    test_method.add_parameter(test_param_name,test_param_type)
    
    try:
        test_method.add_parameter(test_param_name,test_param_type)
        assert False
    except Exception as e:
        assert e == errors.DuplicateParameterException()
    

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

def test_adding_method_overload_duplicate():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_method_return_type = "bool"
    test_params = [("transmission", "CarPart")]

    try:
        test_class.add_method(test_method_name, test_method_return_type, [])
        test_class.add_method(test_method_name, test_method_return_type, test_params)
        test_class.add_method(test_method_name, test_method_return_type, test_params)
        assert False
    except Exception as e:
        assert e == errors.DuplicateMethodOverloadException()

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
    """tests that a method can be renamed using a valid name"""
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
    """"""
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_method_rename = "1type"
    test_method_return_type = "bool"
    test_params = [("transmission", "CarPart")]
    test_method = UmlMethod(test_method_name, test_method_return_type, [])
    test_method.add_parameters(test_params)
    test_val_methods = {test_method_name: {"CarPart": test_method}}

    test_class.add_method(test_method_name, test_method_return_type, test_params)
    try:
        test_class.rename_method(test_method_name, "CarPart", test_method_rename)
        assert False
    except Exception as e:
        assert e == errors.InvalidNameException()
    assert test_class.class_methods == test_val_methods

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

    # add method Drive and Park
    test_class.add_method(test_method_name, test_method_return_type, test_params)
    test_class.add_method(test_method_rename, test_method_return_type, test_params)

    # Rename method Park so it becomes an overload of method Drive
    try:
        test_class.rename_method(test_method_rename, "CarPart", test_method_name)
        assert False
    except Exception as e:
        assert e == errors.DuplicateMethodOverloadException()
    assert test_class.class_methods == test_val_methods
    
## changing method return type
def test_change_method_type_valid():
    """test that the method type changes if the type is valid"""
    test_class = UmlClass("Car", {}, {})
    test_class.add_method("Drive", "bool", [])
    try:
        test_class.change_method_type("Drive", "", "int")
    except Exception as e:
        assert e == None
    assert "int" == test_class.class_methods.get("Drive").get("").return_type
    
def test_change_method_type_invalid_name():
    """test that the method type changes if the type is invalid"""
    test_class = UmlClass("Car", {}, {})
    test_class.add_method("Drive", "bool", [])
    try:
        test_class.change_method_type("Drive", "", "9th")
        assert False
    except Exception as e:
        assert e == errors.InvalidNameException()
    assert "bool" == test_class.class_methods.get("Drive").get("").return_type
    
def test_change_method_type_no_method():
    """test that the change method type errors if no such method"""
    test_class = UmlClass("Car", {}, {})
    test_class.add_method("Drive", "bool", [])
    try:
        test_class.change_method_type("Park", "", "int")
        assert False
    except Exception as e:
        assert e == errors.MethodNameNotExistsException()
    assert "bool" == test_class.class_methods.get("Drive").get("").return_type
    
def test_change_method_type_no_overload():
    """test that change type errors if no overload"""
    test_class = UmlClass("Car", {}, {})
    test_class.add_method("Drive", "bool", [])
    try:
        test_class.change_method_type("Drive", "test", "int")
        assert False
    except Exception as e:
        assert e == errors.MethodOverloadNotExistsException()
    assert "bool" == test_class.class_methods.get("Drive").get("").return_type

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

    test_class.add_method(test_method_name, test_method_return_type, test_params)

    # Invalid method name case
    try:
        test_class.remove_method(test_method_invalid_name, "CarPart")
        assert False
    except Exception as e:
        assert e == errors.MethodNameNotExistsException()
    assert test_class.class_methods == test_val_methods

def test_remove_method_overload_invalid():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_method_return_type = "bool"
    test_params = [("transmission", "CarPart")]
    test_method = UmlMethod(test_method_name, test_method_return_type, [])
    test_method.add_parameters(test_params)
    test_val_methods = {test_method_name: {"CarPart": test_method}}

    test_class.add_method(test_method_name, test_method_return_type, test_params)
    # Invalid overloadID case
    try:
        test_class.remove_method(test_method_name, "")
        assert False
    except Exception as e:
        assert e == errors.MethodOverloadNotExistsException()
    assert test_class.class_methods == test_val_methods

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
    test_class.replace_all_parameters(test_method_name, "", test_params)

    assert test_class.class_methods == test_val_methods

# TODO - Unit tests clear all method parameters
### umlparameter class tests
# test clearing all method parameters
def test_clear_all_method_parameters():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_method_return_type = "bool"
    test_method = UmlMethod(test_method_name, test_method_return_type, [])
    test_val_methods = {test_method_name: {"": test_method}}

    test_class.add_method(test_method_name, test_method_return_type, [])
    test_class.add_parameter(test_method_name, "", "transmission", "CarPart")
    test_class.remove_all_parameters(test_method_name, "CarPart")

    assert test_class.class_methods == test_val_methods

def test_remove_parameter():
    test_class = UmlClass("Car", {}, {})
    test_method_name = "Drive"
    test_method_return_type = "bool"
    test_param = UmlParameter("transmission","Carpart")
    test_method = UmlMethod(test_method_name, test_method_return_type, [test_param])
    
    assert test_param in test_method.params

    test_method.remove_parameter("transmission")
    
    assert test_param not in test_method.params

def test_remove_parameter_not_found():
    test_method_name = "Drive"
    test_method_return_type = "bool"
    test_param = UmlParameter("transmission","Carpart")
    test_method = UmlMethod(test_method_name, test_method_return_type, [test_param])
    
    assert test_param in test_method.params

    try:
        test_method.remove_parameter("nonexistingparam")
        assert False
    except Exception as e:
        assert e == errors.NoSuchParameterException()
    
def test_rename_parameter():
    test_method_name = "Drive"
    test_method_return_type = "bool"
    test_param = UmlParameter("transmission","Carpart")
    test_param2 = UmlParameter("engine","Carpart")
    test_method = UmlMethod(test_method_name, test_method_return_type, [test_param])
    
    assert test_param in test_method.params

    test_method.rename_parameter("transmission","engine")

    assert test_param2 in test_method.params
    
    

def test_rename_parameter_not_found():
    test_method_name = "Drive"
    test_method_return_type = "bool"
    test_param = UmlParameter("transmission","Carpart")
    test_method = UmlMethod(test_method_name, test_method_return_type, [test_param])
    
    assert test_param in test_method.params

    try:
        test_method.rename_parameter("engine","Carpart")
        assert False
    except Exception as e:
        assert e == errors.NoSuchParameterException()

def test_rename_parameter_duplicate():
    test_method_name = "Drive"
    test_method_return_type = "bool"
    test_param = UmlParameter("transmission","Carpart")
    test_method = UmlMethod(test_method_name, test_method_return_type, [test_param])
    
    assert test_param in test_method.params

    try:
        test_method.rename_parameter("engine","transmission")
        assert False
    except Exception as e:
        assert e == errors.DuplicateParameterException()

def test_replace_parameter():
    test_method_name = "Drive"
    test_method_return_type = "bool"
    test_param = UmlParameter("transmission","Carpart")
    test_param2 = UmlParameter("engine","CarPiece")
    test_method = UmlMethod(test_method_name, test_method_return_type, [test_param])
    
    assert test_param in test_method.params

    test_method.replace_parameter("transmission","engine","CarPiece")
    
    assert test_param2 in test_method.params

def test_replace_parameter_duplicate():
    test_method_name = "Drive"
    test_method_return_type = "bool"
    test_param = UmlParameter("transmission","Carpart")
    test_param2 = UmlParameter("engine","CarPiece")
    test_method = UmlMethod(test_method_name, test_method_return_type, [test_param,test_param2])
    
    assert test_param in test_method.params

    try:
        test_method.replace_parameter("transmission","engine","CarPiece")
        assert False
    except Exception as e:
        assert e == errors.DuplicateParameterException()

def test_replace_parameter_Not_found():
    test_method_name = "Drive"
    test_method_return_type = "bool"
    test_param = UmlParameter("transmission","Carpart")
    test_method = UmlMethod(test_method_name, test_method_return_type, [test_param])
    
    assert test_param in test_method.params

    try:
        test_method.replace_parameter("wheel","engine","CarPiece")
        assert False
    except Exception as e:
        assert e == errors.NoSuchParameterException()

### umlclass position method tests
# set_umlclass_position tests
def test_set_umlclass_position_invalid_x_type():
    """tests that an error is raised if the type of the x pos isn't float"""
    try:
        umlclass = UmlClass("temp")
        umlclass.set_umlclass_position("str", 0.0)
        assert False
    except Exception as e:
        assert e == errors.InvalidPositionArgsException()
        
def test_set_umlclass_position_invalid_y_type():
    """tests that an error is raised if the type of the x pos isn't float"""
    try:
        umlclass = UmlClass("temp")
        umlclass.set_umlclass_position(0.0, "str")
        assert False
    except Exception as e:
        assert e == errors.InvalidPositionArgsException()

def test_set_umlclass_position_valid():
    """tests that the position was changed"""
    umlclass = UmlClass("temp")
    try:
        umlclass.set_umlclass_position(2.0, 3.0)
    except Exception as e:
        assert e == None
    assert umlclass.class_pos_x == 2.0
    assert umlclass.class_pos_y == 3.0

# get_umlclass_position tests
def test_get_umlclass_position():
    """tests get pos returns the position"""
    umlclass = UmlClass("temp", {}, {}, 2.0, 3.0)
    pos = None
    try:
        pos = umlclass.get_umlclass_position()
    except Exception as e:
        assert e == None
    assert pos[0] == 2.0
    assert pos[1] == 3.0
### umlclass umlmethod tests

### umlclass umlparamter tests
