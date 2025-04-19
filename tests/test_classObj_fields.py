# Filename: test_classObj_fields.py
# Authors: Juliana Vinluan, John Hershey
# Creation Date: 03-28-2025, Last Edit Date: 04-17-2025
# Description: Unit Tests for umlclass.py field methods

from src.umlclass import UmlClass
from src.umlfield import UmlField
from src import errors
    

def test_add_field_valid():
    """   
    **Valid Field**
        - Input: `Field(name="speed", type="int")`
        - Expected: Pass
    """ 
    test_class = UmlClass("Car",{},{})
    test_field_name = "speed"
    test_field_type = "int"

    try:
        test_class.add_field(test_field_name,test_field_type)
    except Exception as e:
       assert e == errors.InvalidNameException()
    assert "speed" in test_class.class_fields

def test_add_field_camelcase():
    """
    **CamelCase Field Name**
       - Input: `Field(name="MaxSpeed", type="float")`
       - Expected: Pass
    """
    test_class = UmlClass("Car",{},{})
    test_field_name = "MaxSpeed"
    test_field_type = "float"

    try:
        test_class.add_field(test_field_name,test_field_type)
    except Exception as e:
       assert e == errors.InvalidNameException()
    assert "MaxSpeed" in test_class.class_fields

def test_add_field_underscore():
    """
    **Underscore Naming Convention**
       - Input: `Field(name="max_speed", type="int")`
       - Expected: Pass
    """
    test_class = UmlClass("Car",{},{})
    test_field_name = "max_speed"
    test_field_type = "double"
    try:
        test_class.add_field(test_field_name,test_field_type)
    except Exception as e:
       assert e == None
    assert "max_speed" in test_class.class_fields

def test_add_field_single():
    """
    **Single Character Field Name**
       - Input: `Field(name="x", type="int")`
       - Expected: Pass
    """
    test_class = UmlClass("Car",{},{})
    test_field_name = "x"
    test_field_type = "int"

    try:
        test_class.add_field(test_field_name,test_field_type)
    except Exception as e:
       assert e == None
    assert "x" in test_class.class_fields

def test_add_field_complex():
    """
    **Valid Complex Type Names**
       - Input: `Field(name="data", type="int")`
       - Expected: Pass
    """
    test_class = UmlClass("Car",{},{})
    test_field_name = "data"
    test_field_type = "integer"

    try:
        test_class.add_field(test_field_name,test_field_type)
    except Exception as e:
       assert e == errors.InvalidTypeNameException()
    assert "data" in test_class.class_fields

def test_add_field_empty():
    """
    **Empty String as Name**
       - Input: `Field(name="", type="int")`
       - Expected: Error
    """
    test_class = UmlClass("Car",{},{})
    test_field_name = ""
    test_field_type = "int"

    try:
        test_class.add_field(test_field_name,test_field_type)
    except Exception as e:
       assert e == errors.InvalidNameException()
    assert len(test_class.class_fields) == 0

def test_add_field_empty_type(): 
    """
    **Empty String as Type**
        - Input: `Field(name="speed", type="")`
        - Expected: Fail
    """
    test_class = UmlClass("Car",{},{})
    test_field_name = "speed"
    test_field_type = ""

    try:
        test_class.add_field(test_field_name,test_field_type)
        assert False
    except Exception as e:
       assert e == errors.InvalidTypeNameException()
    assert len(test_class.class_fields) == 0

def test_add_field_spaces():
    """
    **Name Contains Spaces**
       - Input: `Field(name="max speed", type="int")`
       - Expected: Error
    """
    test_class = UmlClass("Car",{},{})
    test_field_name = "max speed"
    test_field_type = "int"

    try:
        test_class.add_field(test_field_name,test_field_type)
    except Exception as e:
       assert e == errors.InvalidNameException()
    assert len(test_class.class_fields) == 0

def test_add_field_spaces_type():   
    """
    **Type Contains Spaces**
        - Input: `Field(name="speed", type="int value")`
        - Expected: Error
    """
    test_class = UmlClass("Car",{},{})
    test_field_name = "speed"
    test_field_type = "int value"
    try:
        test_class.add_field(test_field_name,test_field_type)
    except Exception as e:
       assert e == errors.InvalidTypeNameException()
    assert len(test_class.class_fields) == 0

def test_add_field_number():  
    """
    **Name Starts with a Number**
       - Input: `Field(name="123field", type="int")`
       - Expected: invalid name error
    """
    test_class = UmlClass("Car",{},{})
    test_field_name = "123field"
    test_field_type = "int"

    try:
        test_class.add_field(test_field_name,test_field_type)
    except Exception as e:
       assert e == errors.InvalidNameException()
    assert len(test_class.class_fields) == 0

def test_add_field_numeric():
    """
    **Numeric Type as String**
        - Input: `Field(name="speed", type="123")`
        - Expected: Error
    """
    test_class = UmlClass("Car",{},{})
    test_field_name = "speed"
    test_field_type = "123"
    try:
        test_class.add_field(test_field_name,test_field_type)
    except Exception as e:
       assert e == errors.InvalidTypeNameException()
    assert len(test_class.class_fields) == 0

def test_add_field_duplicate():
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
    test_class = UmlClass("Car",{},{})
    test_field_name = "speed"
    test_field_type1 = "int"
    test_field_type2 = "float"

    try:
        test_class.add_field(test_field_name,test_field_type1)
        test_class.add_field(test_field_name,test_field_type2)
    except Exception as e:
       assert e == errors.DuplicateFieldException()
    assert len(test_class.class_fields) == 1

def test_field_invalid():
    """
    **Reserved Keywords as Name**
        - Input: `Field(name="exit", type="int")`
        - Expected: Error
    """
    test_name = "exit"
    test_type = "int"
    test_class = UmlClass("Car",{},{})

    try:
        test_class.add_field(test_name, test_type)
    except Exception as e:
       assert e == None
    assert len(test_class.class_fields) == 1

def test_field_invalid2():
    """
    **Reserved Keywords as Name**
        - Input: `Field(name="speed", type="class")`
        - Expected: Error
    """
    test_name = "speed"
    test_type = "class"
    test_class = UmlClass("Car",{},{})

    try:
        test_class.add_field(test_name, test_type)
    except Exception as e:
       assert e == None
    assert len(test_class.class_fields) == 1

def test_field_long():
    """
    **Very Long Field Name or Type**
        - Input:
          name="this_is_a_very_long_field_name_exceeding_limits"
          type="super_complex_custom_data_type_123")
        - Expected: Enforce length restrictions if necessary
    """
    test_name = "this_is_a_very_long_field_name_exceeding_limits"
    test_type = "super_complex_custom_data_type_123"
    test_class = UmlClass("Car",{},{})

    try:
        test_class.add_field(test_name, test_type)
    except Exception as e:
       assert e == errors.InvalidTypeNameException()
    assert len(test_class.class_fields) == 1

def test_remove_field_valid():
    """
    **Remove Field**
        - Expected: Pass
    """
    #change later to avoid direct assignment of fields
    test_field = UmlField("MaxSpeed","speed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})
    assert len(test_class.class_fields) == 1
    
    try:
        test_class.remove_field(test_field.name)
    except Exception as e:
       assert e == None
    assert len(test_class.class_fields) == 0

def test_remove_field_not_found():
    """
    **Remove non-existing Field**
        - Expected: Fail
    """
    test_field = UmlField("MaxSpeed","speed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})
    assert len(test_class.class_fields) == 1
    try:
        test_class.remove_field("MinSpeed")
    except Exception as e:
       assert e == errors.NoSuchObjectException()
    assert len(test_class.class_fields) == 1

def test_rename_field_valid():
    """
    **Rename Field to valid name**
        - Expected: Pass
    """
    test_field = UmlField("MaxSpeed","speed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})
    
    try:
        test_class.rename_field("MaxSpeed","MinSpeed")
    except Exception as e:
        assert e == None
    assert "MinSpeed" in test_class.class_fields

def test_rename_field_invalid():
    """
    **Rename an field to an invalid name**
        - Expected: Error
    """
    test_field = UmlField("MaxSpeed","speed")
    test_class = UmlClass("Car",{"MaxSpeed":test_field},{})
    
    try:
        test_class.rename_field("MaxSpeed"," speed")
    except Exception as e:
        assert e == errors.InvalidNameException()
    assert "MaxSpeed" in test_class.class_fields

def test_rename_field_existing():
    """
    **Rename a field to an existing field**
        - Expected: Error
    """
    test_field1 = UmlField("MaxSpeed","top_speed")
    test_field2 = UmlField("MinSpeed","slow_speed")
    test_class = UmlClass("Car",{},{})

    try:
        test_class.add_field(test_field1.name,test_field1.type)
        test_class.add_field(test_field2.name,test_field2.type)
        test_class.rename_field("MaxSpeed","MinSpeed")
        assert False
    except Exception as e:
        assert e == errors.DuplicateFieldException()
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