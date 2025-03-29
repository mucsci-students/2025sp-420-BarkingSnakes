# Filename: test_classObj_fields.py
# Authors: Juliana Vinluan
# Creation Date: 03-28-2025, Last Edit Date: 03-28-2025
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
    
"""   
**Valid Field**
    - Input: `Field(name="speed", type="int")`
    - Expected: Pass
""" 
def test_add_field_valid():
    """"""
    test_class = UmlClass("Car",{},{})
    test_field_name = "speed"
    test_field_type = "int"

    try:
        test_class.add_field(test_field_name,test_field_type)
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidNameError"]
    assert "speed" in test_class.class_fields

"""
**CamelCase Field Name**
   - Input: `Field(name="MaxSpeed", type="float")`
   - Expected: Pass
"""
def test_add_field_camelcase():
    test_class = UmlClass("Car",{},{})
    test_field_name = "MaxSpeed"
    test_field_type = "float"

    try:
        test_class.add_field(test_field_name,test_field_type)
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidNameError"]
    assert "MaxSpeed" in test_class.class_fields

"""
**Underscore Naming Convention**
   - Input: `Field(name="max_speed", type="int")`
   - Expected: Pass
"""
def test_add_field_underscore():
    test_class = UmlClass("Car",{},{})
    test_field_name = "max_speed"
    test_field_type = "double"

    try:
        test_class.add_field(test_field_name,test_field_type)
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidNameError"]
    assert "max_speed" in test_class.class_fields

"""
**Single Character Field Name**
   - Input: `Field(name="x", type="int")`
   - Expected: Pass
"""
def test_add_field_single():
    test_class = UmlClass("Car",{},{})
    test_field_name = "x"
    test_field_type = "int"

    try:
        test_class.add_field(test_field_name,test_field_type)
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidNameError"]
    assert "x" in test_class.class_fields

"""
**Valid Complex Type Names**
   - Input: `Field(name="data", type="List[str]")`
   - Expected: Pass
"""
def test_add_field_complex():
    test_class = UmlClass("Car",{},{})
    test_field_name = "data"
    test_field_type = "List[str]"

    try:
        test_class.add_field(test_field_name,test_field_type)
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidNameError"]
    assert "data" in test_class.class_fields

"""
**Empty String as Name**
   - Input: `Field(name="", type="int")`
   - Expected: Error
"""
def test_add_field_empty():
    test_class = UmlClass("Car",{},{})
    test_field_name = ""
    test_field_type = "int"

    try:
        test_class.add_field(test_field_name,test_field_type)
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidNameError"]
    assert len(test_class.class_fields) == 0

"""
**Empty String as Type**
    - Input: `Field(name="speed", type="")`
    - Expected: ???
def test_add_field_empty_type():
    test_class = UmlClass("Car",{},{})
    test_field_name = "speed"
    test_field_type = ""

    try:
        test_class.add_field(test_field_name,test_field_type)
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidTypeNameError"]
    assert len(test_class.class_fields) == 1
"""


"""
**Name Contains Spaces**
   - Input: `Field(name="max speed", type="int")`
   - Expected: Error
"""
def test_add_field_spaces():
    test_class = UmlClass("Car",{},{})
    test_field_name = "max speed"
    test_field_type = "int"

    try:
        test_class.add_field(test_field_name,test_field_type)
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidNameError"]
    assert len(test_class.class_fields) == 0

"""
**Type Contains Spaces**
    - Input: `Field(name="speed", type="int value")`
    - Expected: Error
"""
def test_add_field_spaces_type():
    test_class = UmlClass("Car",{},{})
    test_field_name = "speed"
    test_field_type = "int value"

    try:
        test_class.add_field(test_field_name,test_field_type)
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidTypeNameError"]
    assert len(test_class.class_fields) == 0


"""
**Name Starts with a Number**
   - Input: `Field(name="123field", type="int")`
   - Expected: ???
def test_add_field_number():
    test_class = UmlClass("Car",{},{})
    test_field_name = "123field"
    test_field_type = "int"

    try:
        test_class.add_field(test_field_name,test_field_type)
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidNameError"]
    assert len(test_class.class_fields) == 0
"""

"""
**Numeric Type as String**
    - Input: `Field(name="speed", type="123")`
    - Expected: Error
"""
def test_add_field_numeric():
    test_class = UmlClass("Car",{},{})
    test_field_name = "speed"
    test_field_type = "123"

    try:
        test_class.add_field(test_field_name,test_field_type)
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidTypeNameError"]
    assert len(test_class.class_fields) == 0

"""
**Adding Field to Class with Duplicate Names**
    - Input:
      ```python
      my_class = Class(name="Car")
      my_class.add_field(Field(name="speed", type="int"))
      my_class.add_field(Field(name="speed", type="float"))
      ```
    - Expected: Error
"""
def test_add_field_duplicate():
    test_class = UmlClass("Car",{},{})
    test_field_name = "speed"
    test_field_type1 = "int"
    test_field_type2 = "float"

    try:
        test_class.add_field(test_field_name,test_field_type1)
        test_class.add_field(test_field_name,test_field_type2)
    except Exception as e:
       assert e.get_num() == errors.error_list["DuplicateFieldError"]
    assert len(test_class.class_fields) == 1

"""
**Reserved Keywords as Name**
    - Input: `Field(name="exit", type="int")`
    - Expected: Error
"""
def test_field_invalid():
    test_name = "exit"
    test_type = "int"
    test_class = UmlClass("Car",{},{})

    try:
        test_class.add_field(test_name, test_type)
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidNameError"]
    assert len(test_class.class_fields) == 0

"""
**Reserved Keywords as Name**
    - Input: `Field(name="speed", type="class")`
    - Expected: Error
"""
def test_field_invalid():
    test_name = "speed"
    test_type = "class"
    test_class = UmlClass("Car",{},{})

    try:
        test_class.add_field(test_name, test_type)
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidTypeNameError"]
    assert len(test_class.class_fields) == 0

"""
**Very Long Field Name or Type**
    - Input:
      name="this_is_a_very_long_field_name_exceeding_limits"
      type="super_complex_custom_data_type_123")
    - Expected: Enforce length restrictions if necessary
"""
def test_field_long():
    test_name = "this_is_a_very_long_field_name_exceeding_limits"
    test_type = "super_complex_custom_data_type_123"
    test_class = UmlClass("Car",{},{})

    try:
        test_class.add_field(test_name, test_type)
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidNameError"]
    assert len(test_class.class_fields) == 0


"""
**Remove Field**
    - Expected: Pass
"""
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

"""
**Remove non-existing Field**
    - Expected: Fail
"""
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

"""
**Rename Field to valid name**
    - Expected: Pass"""
def test_rename_field_valid():
    """"""
    test_field = UmlField("MaxSpeed","speed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})
    
    try:
        test_class.rename_field("MaxSpeed","MinSpeed")
    except Exception as e:
        pass
    assert "MinSpeed" in test_class.class_fields

"""
**Rename an field to an invalid name**
    - Expected: Error
"""
def test_rename_field_invalid():
    """"""
    test_field = UmlField("MaxSpeed","speed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})
    
    try:
        test_class.rename_field("Max peed","speed")
    except Exception as e:
        assert e.get_num() == errors.error_list["InvalidNameError"]
    assert "MaxSpeed" in test_class.class_fields

"""
**Rename an field to an invalid type name**
    - Expected: Error
"""
def test_rename_field_invalid():
    """"""
    test_field = UmlField("MaxSpeed","speed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})
    
    try:
        test_class.rename_field("MaxSpeed"," peed")
    except Exception as e:
        assert e.get_num() == errors.error_list["InvalidTypeNameError"]
    assert "MaxSpeed" in test_class.class_fields

"""**Rename a field to an existing field**
    - Expected: Error
"""
def test_rename_field_existing():
    """"""
    test_field1 = UmlField("MaxSpeed","top_speed")
    test_field2 = UmlField("MinSpeed","slow_speed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field1},{"MinSpeed":test_field2})

    try:
        test_class.rename_field("MaxSpeed","MinSpeed")
    except Exception as e:
        assert e.get_num() == errors.error_list["DuplicateFieldError"]
    assert "MaxSpeed" in test_class.class_fields

"""

**Field Name Same as Method Name**
    - Input:
      ```python
      my_class.add_field(Field(name="calculate_speed", type="int"))
      my_class.add_method(Method(name="calculate_speed", return_type="int"))
      ```
    - Expected: Error

"""