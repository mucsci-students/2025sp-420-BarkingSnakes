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
    test_field = UmlField("MaxSpeed","speed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})

    try:
        test_class.rename_field("MaxSpeed","MaxSpeed")
    except Exception as e:
        assert e.get_num() == errors.error_list["DuplicateFieldError"]
    assert "MaxSpeed" in test_class.class_fields

def test_field_valid():
    """"""
    test_name = "speed"
    test_type = "int"
    test_class = UmlClass("Car",{},{})

    try:
        test_class.add_field(test_name, test_type)
    except Exception as e:
        assert e.get_num() == errors.error_list["InvalidNameError"]
    assert test_class.class_fields[test_name].type == test_type

#invalid field name
def test_field_invalid():
    test_name = "exit"
    test_type = "int"
    test_class = UmlClass("Car",{},{})

    try:
        test_class.add_field(test_name, test_type)
    except Exception as e:
       assert e.get_num() == errors.error_list["InvalidNameError"]
    assert len(test_class.class_fields) == 0

"""1. **Valid Field**
   - Input: `Field(name="speed", type="int")`
   - Expected: Pass

2. **CamelCase Field Name**
   - Input: `Field(name="MaxSpeed", type="float")`
   - Expected: Pass

3. **Underscore Naming Convention**
   - Input: `Field(name="max_speed", type="int")`
   - Expected: Pass

4. **Single Character Field Name**
   - Input: `Field(name="x", type="int")`
   - Expected: Pass

5. **Valid Complex Type Names**
   - Input: `Field(name="data", type="List[str]")`
   - Expected: Pass

6. **Empty String as Name**
   - Input: `Field(name="", type="int")`
   - Expected: Error

7. **Name Contains Spaces**
   - Input: `Field(name="max speed", type="int")`
   - Expected: Error

8. **Name Starts with a Number**
   - Input: `Field(name="123field", type="int")`
   - Expected: Error

9. **Name Contains Special Characters**
   - Input: `Field(name="field@", type="int")`
   - Expected: Error

10. **Reserved Keywords as Name**
    - Input: `Field(name="class", type="int")`
    - Expected: Error

11. **Empty String as Type**
    - Input: `Field(name="speed", type="")`
    - Expected: Error

12. **Type Contains Spaces**
    - Input: `Field(name="speed", type="int value")`
    - Expected: Error

13. **Invalid Data Type Name**
    - Input: `Field(name="speed", type="xyz")`
    - Expected: Error

14. **Numeric Type as String**
    - Input: `Field(name="speed", type="123")`
    - Expected: Error

15. **Null Type**
    - Input: `Field(name="speed", type=None)`
    - Expected: Error

16. **Adding Field to Class with Duplicate Names**
    - Input:
      ```python
      my_class = Class(name="Car")
      my_class.add_field(Field(name="speed", type="int"))
      my_class.add_field(Field(name="speed", type="float"))
      ```
    - Expected: Error

17. **Handling Case Sensitivity**
    - Input:
      ```python
      my_class.add_field(Field(name="speed", type="int"))
      my_class.add_field(Field(name="Speed", type="float"))
      ```
    - Expected: Define behavior (case-sensitive or not)

18. **Field Name Same as Method Name**
    - Input:
      ```python
      my_class.add_field(Field(name="calculate_speed", type="int"))
      my_class.add_method(Method(name="calculate_speed", return_type="int"))
      ```
    - Expected: Error

19. **Large Number of Fields in Class**
    - Input: Add 10,000 fields to a class
    - Expected: Should handle efficiently

20. **Very Long Field Name or Type**
    - Input:
      ```python
      Field(name="this_is_a_very_long_field_name_exceeding_limits", type="super_complex_custom_data_type_123")
      ```
    - Expected: Enforce length restrictions if necessary

"""