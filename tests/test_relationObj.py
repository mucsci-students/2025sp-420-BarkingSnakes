# Filename: test_relationObj.py
# Authors: John Hershey
# Creation Date: 2025-03-9, Last Edit Date: 2025-04-18
# Description: Unit Tests for umlrelationship.py 
# as well as relationship methods in umlmodel.py
from src.umlclass import UmlClass
from src.umlrelationship import UmlRelationship, RelationshipType
from src.umlmodel import UmlProject
from src import errors

### relation class tests

def test_valid_types():
    """tests that valid types method return all valid relation types"""
    assert UmlRelationship.valid_relation_types() == "\'aggregation\', \'composition\', \'inheritance\', \'realization\'"

#test __eq__ equality
def test_equality_different_type():
    """tests that relationships with different types are not equal"""
    relation1 = UmlRelationship(RelationshipType.AGGREGATION, UmlClass("temp"), UmlClass("temp1"))
    relation2 = UmlRelationship(RelationshipType.COMPOSITION, UmlClass("temp"), UmlClass("temp1"))
    assert relation1 != relation2
    
def test_equality_different_class():
    """tests that relationships with different classes are not equal"""
    relation1 = UmlRelationship(RelationshipType.COMPOSITION, UmlClass("temp3"), UmlClass("temp2"))
    relation2 = UmlRelationship(RelationshipType.COMPOSITION, UmlClass("temp"), UmlClass("temp1"))
    assert relation1 != relation2
    
def test_equality_same_class():
    """tests that relationships with same type and classes are equal"""
    relation1 = UmlRelationship(RelationshipType.AGGREGATION, UmlClass("temp"), UmlClass("temp1"))
    relation2 = UmlRelationship(RelationshipType.AGGREGATION, UmlClass("temp"), UmlClass("temp1"))
    assert relation1 == relation2
    
def test_equality_mirrored_class():
    """tests that relationships with reversed classes are not equal"""
    relation1 = UmlRelationship(RelationshipType.AGGREGATION, UmlClass("temp1"), UmlClass("temp1"))
    relation2 = UmlRelationship(RelationshipType.AGGREGATION, UmlClass("temp"), UmlClass("temp"))
    assert relation1 != relation2
    
### relation method tests
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
        type = UmlProject()._relationship_type_from_str("0")
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
    try:
        model = UmlProject()
        model.add_relationship("temp", "temp2", "1")
    except Exception as e:
        var = 1
        assert e == errors.NoSuchObjectException()
    assert var
    assert len(model.relationships) == 0
    
def test_add_relation_one_classes():
    """tests that an error is raised if a class in relation doesn't exist"""
    var = None
    try:
        model = UmlProject()
        model.add_umlclass("temp")
        model.add_relationship("temp", "temp2", "1")
    except Exception as e:
        var = 1
        assert e == errors.NoSuchObjectException()
    assert var
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
        assert e == None
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
        model.add_relationship("temp", "temp2", "2")
    except Exception as e:
        var = 1
        assert e == errors.DuplicateRelationshipException()
    assert var
    assert len(model.relationships) == 1

def test_add_relation_duplicate_type():
    """tests that an error is raised if the src/dest and type is a duplicate"""
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

def test_add_relation_bidirectional():
    """tests that relation is added even if one exists in other direction"""
    var = None
    try:
        model = UmlProject()
        model.add_umlclass("temp")
        model.add_umlclass("temp2")
        model.add_relationship("temp", "temp2", "1")
        model.add_relationship("temp2", "temp", "2")
    except Exception as e:
        var = 1
        assert e == None
    assert not var
    assert len(model.relationships) == 2
    
# set_type_relation tests
def test_set_relation_no_relation():
    """tests that an error is raised if no relation exists"""
    var = None
    model = None
    try:
        model = UmlProject()
        model.add_umlclass("temp")
        model.add_umlclass("temp2")
        model.set_type_relationship("temp", "temp2", "1")
    except Exception as e:
        var = 1
        assert e == errors.NoSuchObjectException()
    assert var
    assert len(model.relationships) == 0
    
def test_set_relation_type_no_such_relation_or_classes():
    """tests that an error is raised if classes don't exist"""
    var = None
    model = None
    try:
        model = UmlProject()
        model.set_type_relationship("temp", "temp2", "1")
    except Exception as e:
        var = 1
        assert e == errors.NoSuchObjectException()
    assert var
    assert len(model.relationships) == 0

def test_set_relation_no_such_relation():
    """tests that an error is raised if that relation does not exist"""
    var = None
    model = None
    try:
        model = UmlProject()
        model.add_umlclass("temp")
        model.add_umlclass("temp2")
        model.add_relationship("temp2", "temp", "1")
        model.set_type_relationship("temp", "temp2", "1")
    except Exception as e:
        var = 1
        assert e == errors.NoSuchObjectException()
    assert var
    assert len(model.relationships) == 1
    
def test_set_relation_type_exists():
    """tests that no error is raised if type specified is the same"""
    var = None
    model = None
    try:
        model = UmlProject()
        model.add_umlclass("temp")
        model.add_umlclass("temp2")
        model.add_relationship("temp", "temp2", "1")
        model.set_type_relationship("temp", "temp2", "1")
    except Exception as e:
        var = 1
        assert e == None
    assert not var
    assert len(model.relationships) == 1
    
def test_set_relation_type_exists():
    """tests that relation type is changed"""
    var = None
    model = None
    try:
        model = UmlProject()
        model.add_umlclass("temp")
        model.add_umlclass("temp2")
        model.add_relationship("temp", "temp2", "1")
        model.set_type_relationship("temp", "temp2", "2")
    except Exception as e:
        var = 1
        assert e == None
    assert not var
    assert len(model.relationships) == 1
    #get relationship type from model relation list
    assert model.relationships.pop().relationship_type.value == 2
    
def test_set_relation_type_invalid_num():
    """tests that an error is raised if type is invalid"""
    model = None
    try:
        model = UmlProject()
        model.add_umlclass("temp")
        model.add_umlclass("temp2")
        model.add_relationship("temp", "temp2", "1")
        model.set_type_relationship("temp", "temp2", "the")
        assert False
    except Exception as e:
        assert e == errors.InvalidRelationshipTypeException()
    assert len(model.relationships) == 1
    #get relationship type from model relation list
    assert model.relationships.pop().relationship_type.value == 1

# delete_relation tests
def test_delete_relation_none_class():
    """tests that an error is raised if an input class is None"""
    try:
        UmlProject().delete_relationship(None, "temp2")
        assert False
    except Exception as e:
        assert e == errors.NullObjectException()

def test_delete_relation_no_classes():
    """tests that an error is raised if no input classes exist"""
    try:
        model = UmlProject()
        model.delete_relationship("temp", "temp2")
        assert False
    except Exception as e:
        assert e == errors.NoSuchObjectException()
        
def test_delete_relation_one_class():
    """tests that an error is raised if one input class doesn't exist"""
    try:
        model = UmlProject()
        model.add_umlclass("temp")
        model.delete_relationship("temp", "temp2")
        assert False
    except Exception as e:
        assert e == errors.NoSuchObjectException()
    assert "temp" in model.classes

def test_delete_relation_no_relations():
    """tests that an error is raised if no relations exist"""
    model = None
    try:
        model = UmlProject()
        model.add_umlclass("temp")
        model.add_umlclass("temp2")
        model.delete_relationship("temp", "temp2")
        assert False
    except Exception as e:
        assert e == errors.NoSuchObjectException()
    assert "temp" in model.classes
        
def test_delete_relation_no_such_relation():
    """tests that an error is raised if an input relation doesn't exist"""
    model = None
    try:
        model = UmlProject()
        model.add_umlclass("temp")
        model.add_umlclass("temp2")
        model.add_relationship("temp2", "temp", "1")
        model.delete_relationship("temp", "temp2")
        assert False
    except Exception as e:
        assert e == errors.NoSuchObjectException()
    assert len(model.relationships) == 1
    
def test_delete_relation():
    """tests that relation is deleted"""
    model = None
    try:
        model = UmlProject()
        model.add_umlclass("temp")
        model.add_umlclass("temp2")
        model.add_relationship("temp", "temp2", "1")
        assert len(model.relationships) == 1
        model.delete_relationship("temp", "temp2")
    except Exception as e:
        assert e == None
    assert len(model.relationships) == 0