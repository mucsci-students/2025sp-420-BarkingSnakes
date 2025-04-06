# Filename: test_relationObj.py
# Authors: John Hershey
# Creation Date: 2025-03-9, Last Edit Date: 2025-04-06
# Description: Unit Tests for umlrelationship.py
from src.umlclass import UmlClass
from src.umlrelationship import UmlRelationship, RelationshipType
from src.umlmodel import UmlProject
from src import errors

def test_circular_relation():
    """tests that a circular relationship doesn't raise an error"""
    var = None
    try:
        class1 = UmlClass("name")
        UmlRelationship(0,class1, class1)
    except Exception as e:
        var = 1
        assert e == None
    assert not var
    
# relation_from_str tests
def test_relation_type_from_str_null():
    """tests that an error is raised if the type is invalid"""
    var = None
    try:
        UmlProject()._relationship_type_from_str(None)
    except Exception as e:
        var = 1
        assert e == errors.NullObjectException()
    assert var
    
def test_relation_type_from_str_invalid():
    """tests that an error is raised if the type is invalid"""
    var = None
    try:
        UmlProject()._relationship_type_from_str("test")
    except Exception as e:
        var = 1
        assert e == errors.InvalidRelationshipTypeException()
    assert var

def test_relation_type_from_str_valid_str():
    """tests that no error is raised if the type is valid"""
    var = None
    try:
        type = UmlProject()._relationship_type_from_str("aggregation")
    except Exception as e:
        var = 1
        assert e == None
    assert type.value == RelationshipType.AGGREGATION.value
    assert not var
    
def test_relation_type_from_str_valid_int():
    """tests that no error is raised if the type is valid int string"""
    var = None
    try:
        type = UmlProject()._relationship_type_from_str("1")
    except Exception as e:
        var = 1
        assert e == None
    assert type.value == RelationshipType.AGGREGATION.value
    assert not var
    
def test_relation_type_from_str_invalid_int():
    """tests that error is raised if the type is invalid int string"""
    var = None
    type = None
    try:
        type = UmlProject()._relationship_type_from_str("8")
    except Exception as e:
        var = 1
        assert e == errors.InvalidRelationshipTypeException()
    assert not type
    assert var
    
def test_relation_type_from_str_default():
    """tests that error is raised if the type default, which is invalid"""
    var = None
    type = None
    try:
        type = UmlProject()._relationship_type_from_str(str(RelationshipType.DEFAULT))
    except Exception as e:
        var = 1
        assert e == errors.InvalidRelationshipTypeException()
    assert not type
    assert var

# get_relation tests
def test_get_relation_null_class():
    """tests that an error is raised if input class was null"""
    var = None
    try:
        UmlProject().get_relationship("temp",None)
    except Exception as e:
        var = 1
        assert e == errors.NullObjectException()
    assert var
    
def test_get_relation_no_classes():
    """tests that an error is raised if classes in relation don't exist"""
    var = None
    try:
        model = UmlProject()
        model.get_relationship("temp", "temp2")
    except Exception as e:
        var = 1
        assert e == errors.NoSuchObjectException()
    assert var
    
def test_get_relation_one_class():
    """tests that an error is raised one of the classes in a relation doesn't exist"""
    var = None
    try:
        model = UmlProject()
        model.add_umlclass("temp")
        model.get_relationship("temp", "temp2")
    except Exception as e:
        var = 1
        assert e == errors.NoSuchObjectException()
    assert var

def test_get_relation_no_relation():
    """tests that an error is raised if a relation doesn't exist"""
    var = None
    model = None
    try:
        model = UmlProject()
        model.add_umlclass("temp")
        model.get_relationship("temp", "temp")
    except Exception as e:
        var = 1
        assert e == errors.NoSuchObjectException()
    assert var
    assert "temp" in model.classes
    
def test_get_relation_exists():
    """tests that no error is raised if a relation exists"""
    var = None
    relation = None
    try:
        model = UmlProject()
        model.add_umlclass("temp")
        model.add_relationship("temp", "temp", "1")
        relation = model.get_relationship("temp", "temp")
    except Exception as e:
        var = 1
        assert e == None
    assert not var
    assert relation
    assert relation in model.relationships

# add_relation tests
def test_add_relation_null_class():
    """tests that null object error is raised if class is None"""
    var = None
    try:
        model = UmlProject()
        model.add_umlclass("temp")
        #"1" is value of aggregation type
        model.add_relationship("temp", None, "1")
    except Exception as e:
        var = 1
        assert e == errors.NullObjectException()
    assert var
    assert len(model.relationships) == 0
    
def test_add_relation_null_type():
    """tests that no error is raised"""
    var = None
    try:
        model = UmlProject()
        model.add_umlclass("temp")
        #"1" is value of aggregation type
        model.add_relationship("temp", "temp", None)
    except Exception as e:
        var = 1
        assert e == errors.NullObjectException()
    assert var
    assert len(model.relationships) == 0
    
def test_add_relation_no_classes():
    """tests that an error is raised if classes in relation don't exist"""
    var = None
    relation = None
    try:
        model = UmlProject()
        relation = model.add_relationship("temp", "temp2", "1")
    except Exception as e:
        var = 1
        assert e == errors.NoSuchObjectException()
    assert var
    assert not relation
    assert len(model.relationships) == 0
    
def test_add_relation():
    """tests that no error is raised"""
    var = None
    try:
        model = UmlProject()
        model.add_umlclass("temp")
        model.add_umlclass("temp2")
        model.add_relationship("temp", "temp2", "1")
    except Exception as e:
        var = 1
        assert e == errors.NoSuchObjectException()
    assert not var
    assert len(model.relationships) == 1

def test_add_relation_duplicate():
    """tests that an error is raised if the relation is a duplicate"""
    var = None
    try:
        model = UmlProject()
        model.add_umlclass("temp")
        model.add_umlclass("temp2")
        model.add_relationship("temp", "temp2", "1")
        model.add_relationship("temp", "temp2", "1")
    except Exception as e:
        var = 1
        assert e == errors.DuplicateRelationshipException()
    assert var
    assert len(model.relationships) == 1
    
# set_type_relation tests

# delete_relation tests