# Filename: test_save_load.py
# Authors: Steven Barnes, John Hershey
# Date: 2025-02-25, Last edit date: 2025-05-12
# Description: Unit tests for the saving and loading json,
#   as well as schema validation and json dict parsing

import os
import json

from src import errors
from src.umlmodel import UmlProject
from src.umlcontroller import UmlController
from src.views.umlview_test import UmlTestView

###loading tests
def test_load_no_existing_file():
    """tests that an invalid file error is given when loading a fake file"""
    #temp variable for proving exeption
    var=None
    try:
        UmlProject().load("fake.json")
    except Exception as e:
        var=1
        assert e == errors.InvalidFileException()
    #make sure an exception was raised
    assert var
    
def test_load_invalid_file():
    """tests that an invalid file error is given when loading a non-json file"""
    #temp variable for proving exeption
    var=None
    try:
        UmlProject().load("Readme.ME")
    except Exception as e:
        var=1
        assert e == errors.InvalidFileException()
    #make sure an exception was raised
    assert var
    
def test_load_dir():
    """make sure an error was raised when a directory is given as a filepath"""
    try:
        model = UmlProject()
        model.load("src")
        assert False
    except Exception as e:
        assert e == errors.InvalidFileException()

def test_load_invalid_Json_file(tmp_path):
    """Tests that an invalid file error is given when loading a file that violates the JSON schema"""

    try:
        invalid_data = {"badkey": "badvalue"}
        invalid_file = tmp_path / "invalid_schema.json"
        
        with open(invalid_file, "w") as f:
            json.dump(invalid_data, f)

            UmlProject().load(str(invalid_file))
        assert False
    except Exception as e:
        assert e == errors.InvalidJsonSchemaException()
    

def test_make_no_new_file():
    """test a new file was not made"""
    var = None
    try:
        # app = UmlApplication()
        app = UmlController(UmlTestView())
        app.new_project("test.json")
        with open("test.json", "r") as f:
            # make sure file doesn't exists
            assert not f.read()
            
    except Exception as e:
        var = 1
        assert e.__class__ == FileNotFoundError
    #make sure an exception was raised
    assert var

def test_save_no_existing_file():
    """test that no error is given when saving to a 
        filename that does not yet exist"""
    var = None
    proj = UmlProject()
    try:
        proj._save_path = "test.json"
        #save does not need a filename if path is already set
        proj.save()
        assert os.path.exists("test.json")
    except Exception as e:
        var = 1
        assert e == None
    assert not var

def test_save_no_save_path():
    """test when saving with not save path"""
    var = None
    proj = UmlProject()
    try:
        proj._save_path = None
        #save does not need a filename if path is already set
        proj.save()
        assert False
    except Exception as e:
        assert e == errors.NoActiveProjectException()

def test_load_existing_file():
    """test a file that exists can be loaded"""
    try:
        proj = UmlProject()
        proj.load("test.json")
        assert proj.classes != None
    except Exception as e:
        assert e == None

def test_save_existing_file():
    """test that a file will be updated when saved"""
    var = 1
    try:
        app = UmlController(UmlTestView())
        app.load_project("test.json")
        #adds the umlclass with name temp
        # app.active_class = "temp"
        app.command_add_umlclass("temp")
        app.model.save()
        assert "temp" in app.model.classes
        var = 2
        #loads the file again and checks if the change was saved
        app.load_project("test.json")
        # app.command_class("temp")
        #try to add the class again
        app.command_add_umlclass("temp")
        var = 3
    except Exception as e:
        var = None
        assert e == errors.DuplicateClassException()
    
    assert not var

def test_new_old_file_exists():
    """test an existing file is not overridden 
    when project with that name is made, only when saved"""
    var = None
    try:
        app = UmlController(UmlTestView())
        app.new_project("test.json", True)
        #another app to check file state
        # app2 = UmlApplication()
        app2 = UmlController(UmlTestView())
        app2.load_project("test.json", True)
        #assert class remains
        assert "temp" in app2.model.classes
        # app-level save prompts user, so until prints are handled by
        # tests - a view-implementation-solvable issue, use project save
        app.model.save()
        app2.load_project("test.json", True)
        assert "temp" not in app2.model.classes
    except Exception as e:
        var = 1
        assert e == None
    assert not var

#set_save_path
def test_set_save_path_no_file():
    """make sure that no error is raised if no filename is given"""
    model = UmlProject()
    try:
        model.set_save_path("")
    except Exception as e:
        assert e == None
    assert model._save_path == ""
    
def test_set_save_path_no_file_still_change():
    """make sure that no error is raised if no filename is given"""
    model = UmlProject()
    try:
        model._save_path = "temp"
        model.set_save_path("")
    except Exception as e:
        assert e == None
    assert model._save_path == ""
    
def test_set_save_path_not_json():
    """make sure that an error is raised if the given file is not json"""
    model = UmlProject()
    try:
        model.set_save_path("wrong")
    except Exception as e:
        assert e == errors.InvalidFileException()
    assert model._save_path == None
    
def test_set_save_path_not_json_not_changed():
    """make sure that an error is raised if the filename is invalid, 
        and the save path is not changed"""
    model = UmlProject()
    try:
        model._save_path ="path"
        model.set_save_path("wrong")
    except Exception as e:
        assert e == errors.InvalidFileException()
    assert model._save_path == "path"

#_is_json_file
def test_is_json_file_not_json():
    """make sure an error is raised when the filename isn't a json"""
    try:
        model = UmlProject()
        model._is_json_file("test")
        assert False
    except Exception as e:
        assert e == errors.InvalidFileException()
        
def test_is_json_file_is_json():
    """make sure no error is raised when the filename is a json"""
    try:
        model = UmlProject()
        model._is_json_file("test.json")
    except Exception as e:
        assert e == None
        
### parsing tests
#parse_uml_data
def test_parse_data_valid_empty():
    """test that data containing proper components doesn't error"""
    try:
        data = {"classes": [],"relationships": []}
        model = UmlProject()
        model._parse_uml_data(data)
    except Exception as e:
        assert e == None
        
def test_parse_data_valid():
    """test that data containing proper components doesn't error"""
    try:
        data = {"classes":[{"name": "temp","fields": [],"methods": [],"position": {"x": 0.0,"y": 0.0}}],
         "relationships": [{"source": "temp","destination": "temp","type": "Aggregation"}]}
        model = UmlProject()
        model._parse_uml_data(data)
    except Exception as e:
        assert e == None
        
def test_parse_data_missing_class_entry():
    """test that data missing the classes field has an error"""
    try:
        data = {"relationships": []}
        model = UmlProject()
        model._parse_uml_data(data)
        assert False
    except Exception as e:
        assert e == errors.InvalidJsonSchemaException()
        
def test_parse_data_valid_duplicate_class():
    """test that data containing an extra class errors"""
    try:
        data = {"classes": [{"name": "temp","fields": [],"methods": [],"position": {"x": 0.0,"y": 0.0}},
                            {"name": "temp","fields": [],"methods": [],"position": {"x": 3.0,"y": 7.0}}],
                "relationships": []}
        model = UmlProject()
        model._parse_uml_data(data)
        assert False
    except Exception as e:
        assert e == errors.InvalidJsonSchemaException()
        
def test_parse_data_valid_duplicate_relations():
    """test that data containing proper components doesn't error"""
    try:
        data = {"classes":[{"name": "temp","fields": [],"methods": [],"position": {"x": 0.0,"y": 0.0}}],
         "relationships": [{"source": "temp","destination": "temp","type": "Aggregation"}, 
                           {"source": "temp","destination": "temp","type": "Aggregation"}]}
        model = UmlProject()
        model._parse_uml_data(data)
    except Exception as e:
        assert e == errors.InvalidJsonSchemaException()
        assert len(model.relationships) == 1
        
# parse_uml_class
def test_parse_data_valid_empty():
    """test that umlclass data containing proper components doesn't error"""
    try:
        data = {"name": "temp","fields": [],"methods": [],"position": {"x": 0.0,"y": 0.0}}
        model = UmlProject()
        umlclass = model._parse_uml_class(data)
    except Exception as e:
        assert e == None
    assert umlclass.class_name == "temp"
    
def test_parse_data_invalid_empty_brackets_fields():
    """test that umlclass data containing proper components does error"""
    try:
        data = {"name": "temp","fields": [{}],"methods": [],"position": {"x": 0.0,"y": 0.0}}
        model = UmlProject()
        umlclass = model._parse_uml_class(data)
    except Exception as e:
        assert e == errors.InvalidJsonSchemaException()
    
def test_parse_data_invalid_empty_brackets_methods():
    """test that umlclass data containing proper components does error"""
    try:
        data = {"name": "temp","fields": [],"methods": [{}],"position": {"x": 0.0,"y": 0.0}}
        model = UmlProject()
        umlclass = model._parse_uml_class(data)
    except Exception as e:
        assert e == errors.InvalidJsonSchemaException()
    assert not umlclass.class_fields

#parse_uml_relationship
def test_parse_relation_data_valid_one_class():
    """test that data containing proper components doesn't error"""
    try:
        data = {"source": "temp","destination": "temp","type": "Aggregation"}
        model = UmlProject()
        model.add_umlclass("temp")
        model._parse_uml_relationship(data)
    except Exception as e:
        assert e == None
        
def test_parse_relation_data_valid_two_classes():
    """test that data containing proper components with two classes doesn't error"""
    try:
        data = {"source": "temp","destination": "temp2","type": "Aggregation"}
        model = UmlProject()
        model.add_umlclass("temp")
        model.add_umlclass("temp2")
        model._parse_uml_relationship(data)
    except Exception as e:
        assert e == None
        
def test_parse_relation_data_missing_class():
    """test that data with a class that doesn't exist errors"""
    try:
        data = {"source": "temp","destination": "temp","type": "Aggregation"}
        model = UmlProject()
        model._parse_uml_data(data)
        assert False
    except Exception as e:
        assert e == errors.InvalidJsonSchemaException()
        
def test_parse_relation_data_invalid_type():
    """test that data containing the wrong type has an error"""
    try:
        data = {"source": "temp","destination": "temp","type": "Wrong"}
        model = UmlProject()
        model.add_umlclass("temp")
        model._parse_uml_data(data)
    except Exception as e:
        assert e == errors.InvalidJsonSchemaException()
        
def test_parse_relation_data_valid_one_class():
    """test that data containing a class that doesn't exist raises an error"""
    try:
        data = {"source": "temp","destination": "temp2","type": "Aggregation"}
        model = UmlProject()
        model.add_umlclass("temp")
        model._parse_uml_data(data)
        assert False
    except Exception as e:
        assert e == errors.InvalidJsonSchemaException()

### schema validation tests
def test_validate_schema_valid():
    """test that a schema matching the template raises no errors"""
    try:
        data = {"classes": [],"relationships": []}
        assert UmlProject().validate_json_schema(data)
    except Exception as e:
        assert e == None

def test_validate_schema_valid_with_class():
    """test that a schema matching the template raises no errors"""
    try:
        data = {"classes": [{"name": "temp", "fields": [],"methods": [],
                "position": {"x": 0.0,"y": 0.0}}],"relationships": []}
        assert UmlProject().validate_json_schema(data)
    except Exception as e:
        assert e == None

def test_validate_schema_missing_class():
    """test that a schema missing one of the basic fields will error"""
    try:
        data = {"relationships": []}
        UmlProject().validate_json_schema(data)
        assert False
    except Exception as e:
        assert e == errors.InvalidJsonSchemaException()
        
def test_validate_schema_missing_class_pos():
    """test that a schema with one of the classes missing data crashes"""
    try:
        data = {"classes": [{"name": "temp", "fields": [],"methods": []}],
                "relationships": []}
        UmlProject().validate_json_schema(data)
        assert False
    except Exception as e:
        assert e == errors.InvalidJsonSchemaException()
        
def test_validate_schema_extra_data():
    """test that a schema with an extra field raises an error"""
    try:
        data = {"classes": [],"relationships": [], "extra": "data"}
        UmlProject().validate_json_schema(data)
        assert False
    except Exception as e:
        assert e == errors.InvalidJsonSchemaException()
        
def test_validate_schema_wrong_class_data():
    """test that a schema with the wrong class data errors"""
    try:
        data = {"classes": [{"name": "temp", "fields": [],"methods": [],
                "position": {"x": 0.0,"y": 0.0}}, {"wrong"}],"relationships": []}
        UmlProject().validate_json_schema(data)
        assert False
    except Exception as e:
        assert e == errors.InvalidJsonSchemaException()
        
def test_validate_filepath_dir():
    """tests that a dir raises an error"""
    try:
        UmlProject()._validate_filepath("/src")
    except Exception as e:
        assert e == errors.InvalidFileException()
    
### delete test file 
def test_delete():
    """delete the file after other tests are run"""
    os.remove("test.json")
    