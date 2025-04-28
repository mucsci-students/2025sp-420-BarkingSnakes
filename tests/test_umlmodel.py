# Filename: test_umlmodel.py
# Authors: Steven Barnes, John Hershey, Evan Magill, Kyle Kalbach, Juliana Vinluan, Spencer Hoover
# Creation Date: 04-06-2025, Last Edit Date: 04-27-2025
# Description: Unit Tests for umlmodel.py
from src.umlmodel import UmlProject
from src import errors

# rename class tests
def test_rename_umlclass():
    """Tests rename umlclass"""
    test_proj = UmlProject()
    test_proj.add_umlclass("testclass")

    test_proj.rename_umlclass("testclass","testclass2")

    assert "testclass2" in test_proj.classes

def test_rename_umlclass_nonexistant_class():
    """Tests rename umlclass nosuchobjecterror"""
    test_proj = UmlProject()
    test_proj.add_umlclass("testclass")

    try:
        test_proj.rename_umlclass("testclass1","testclass2")
        assert False
    except Exception as e:
        assert e == errors.NoSuchObjectException()

def test_rename_umlclass_existing_class():
    """Tests rename umlclass duplicateclasserror"""
    test_proj = UmlProject()
    test_proj.add_umlclass("testclass")
    test_proj.add_umlclass("car")

    try:
        test_proj.rename_umlclass("testclass","car")
        assert False
    except Exception as e:
        assert e == errors.DuplicateClassException()

# delete class tests
def test_delete_umlclass():
    """Tests delete_umlclass"""
    test_proj = UmlProject()
    test_proj.add_umlclass("car")
    test_proj.delete_umlclass("car")

    assert "car" not in test_proj.classes

def test_delete_umlclass_nonexistant_class():
    """Tests delete_umlclass"""
    test_proj = UmlProject()
    test_proj.add_umlclass("car")
    
    try:
        test_proj.delete_umlclass("van")
        assert False
    except Exception as e:
        assert e == errors.NoSuchObjectException()
    
def test_add_field():
    """Tests add_field"""
    test_proj = UmlProject()
    test_proj.add_umlclass("car")
    test_proj.add_field("car","MaxSpeed","mph")
    
    test_class = test_proj.classes.pop("car")

    assert "MaxSpeed" in test_class.class_fields

def test_add_field():
    """Tests add_field"""
    test_proj = UmlProject()
    test_proj.add_umlclass("car")
    test_proj.add_field("car","MaxSpeed","mph")
    
    try:
        test_proj.add_field("car","MaxSpeed","mph")
        assert False
    except Exception as e:
        assert e == errors.DuplicateFieldException()

def test_rename_field():
    """Tests rename_field"""
    test_proj = UmlProject()
    test_proj.add_umlclass("car")
    test_proj.add_field("car","MaxSpeed","mph")

    test_proj.rename_field("car","MaxSpeed","MinSpeed")

    assert "MinSpeed" in  test_proj.classes.get("car").class_fields
    assert "MaxSpeed" not in  test_proj.classes.get("car").class_fields
    
def test_change_field_type():
    """Tests change_field_type"""
    test_proj = UmlProject()
    test_proj.add_umlclass("car")
    test_proj.add_field("car","MaxSpeed","mph")

    test_proj.change_field_type("car","MaxSpeed","kmph")
    umlclass = test_proj.classes.get("car")
    assert "kmph" == umlclass.class_fields.get("MaxSpeed").type

def test_delete_field():
    """Tests delete_field"""
    test_proj = UmlProject()
    test_proj.add_umlclass("car")
    test_proj.add_field("car","MaxSpeed","mph")

    test_proj.delete_field("car","MaxSpeed")

    assert "MaxSpeed" not in  test_proj.classes.get("car").class_fields

# update class position tests

def test_update_position_class_no_such_class():
    """Tests that an error is raised if the class isn't in the project"""
    model = UmlProject()
    try:
        model.add_umlclass("temp")
        model.update_position_umlclass("temp2", 1.0, 2.0)
        assert False
    except Exception as e:
        assert e == errors.NoSuchObjectException()
    # make sure existing class wasn't changed
    assert model.get_umlclass("temp").get_umlclass_position() == (0.0, 0.0)
    assert not model.classes.get("temp2")

def test_update_position_class_invalid_type():
    """Tests that an error is raised if a position type isn't float"""
    model = UmlProject()
    try:
        model.add_umlclass("temp")
        model.update_position_umlclass("temp", "str", 2.0)
        assert False
    except Exception as e:
        assert e == errors.InvalidPositionArgsException()
    assert model.get_umlclass("temp").get_umlclass_position() == (0.0, 0.0)
    
def test_update_position_class():
    """Tests that no error is raised if class exists and positions are valid"""
    model = UmlProject()
    try:
        model.add_umlclass("temp")
        model.update_position_umlclass("temp", 1.0, 2.0)
    except Exception as e:
        assert e == None
    assert model.get_umlclass("temp").get_umlclass_position() == (1.0, 2.0)

# get class position tests
def test_get_position_class_no_class():
    """Tests that an error is raised if class does not exist"""
    model = UmlProject()
    try:
        model.add_umlclass("temp")
        model.get_position_umlclass("temp2")
        assert False
    except Exception as e:
        assert e == errors.NoSuchObjectException()
        
def test_get_position_class_exists():
    """Tests that no error is raised if class exists"""
    pos = None
    try:
        model = UmlProject()
        model.add_umlclass("temp")
        model.update_position_umlclass("temp", 1.0, 2.0)
        pos = model.get_position_umlclass("temp")
    except Exception as e:
        assert e == None
    assert pos == (1.0,2.0)

### method tests

def test_change_method_type():
    """Tests change_method_type"""
    test_proj = UmlProject()
    test_proj.add_umlclass("car")
    test_proj.add_method("car","MaxSpeed","mph", [])

    test_proj.change_method_type("car","MaxSpeed","kmph", "")
    umlclass = test_proj.classes.get("car")
    assert "kmph" == umlclass.class_methods.get("MaxSpeed").get("").return_type