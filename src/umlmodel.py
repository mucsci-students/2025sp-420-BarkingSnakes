# Filename: uml.py
# Authors: Steven Barnes, John Hershey, Evan Magill, Kyle Kalbach
# Date: 2025-02-14
# Description: Entry point for UML editor program.

from __future__ import annotations

import functools
import os
import json
import re
import logging
import jsonschema
import jsonschema.exceptions

import errors
from umlclass import UmlClass, UmlField
from umlmethod import UmlParameter, UmlMethod
from umlrelationship import UmlRelationship, RelationshipType

#project directory path
__DIR__ = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(__DIR__, "templates", "umlschema.json")
REGEX_DEFAULT = "^[A-Za-z][A-Za-z0-9_]*$"

class UmlProject:
    """"""
    def __init__(self):
        self.classes:dict[str,UmlClass] = {}
        self.relationships:set[UmlRelationship] = set()
        self._save_path = None
        self.has_unsaved_changes = False

    def _regex_pattern(count:int = 1, pattern:str = REGEX_DEFAULT):
        print(count, pattern)
        def regex_decorator(func):
            @functools.wraps(func)
            def wrapper(self:UmlProject, *args, **kwargs):
                print(count, args)
                for i in range(count):
                    if re.search(pattern, args[i]) is None:
                        raise errors.InvalidNameException()
                return func(self, *args, **kwargs)
            return wrapper
        return regex_decorator
    
    def _has_changed(func):
        @functools.wraps(func)
        def wrapper(self:UmlProject, *args, **kwargs):
            self.has_unsaved_changes = True
            return func(self, *args, **kwargs)
        return wrapper


    def new(self) -> None:
        """Create a new project from template.

        Params: 
            None
        Returns:
            None
        Exceptions:
            None
        """
        template_path = os.path.join(__DIR__, 'templates', 'uml_project_template.json')
        #open needs moved to save section in model
        with open(template_path, "r") as t:
            data = json.load(t)
            self.validate_json_schema(data)
            self._parse_uml_data(data)
    
    def load(self, filepath:str) -> int:
        """Load the project at the provided filepath.

        Params: 
            filepath: string
        Returns:
            int: 0 if success
        Exceptions:
            InvalidFileException
        """
        #method returns 0 when true, which is equivalent to false
        #if not 0 errors should be called in validate
        if self._validate_filepath(filepath):
            raise errors.InvalidFileException()
        
        with open(filepath, "r") as f:
            data =  json.load(f)
            self.validate_json_schema(data)
            self._parse_uml_data(data)
        #use when saving later
        self._save_path = filepath

        return 0
    
    def save(self) -> int:
        """Saves the currently opened project, 
        using the same filepath it was loaded from.

        Params: 
            None
        Returns:
            int: 0 if successful.
        Exceptions:
            NoActiveProjectException
        """
        if not self._save_path:
            raise errors.NoActiveProjectException()
        
        self.validate_json_schema(self._save_object)
        #will override, handled by caller(umlapplication)
        with open(self._save_path, "w") as f:
            json.dump(self._save_object, f, indent=4)
        self.has_unsaved_changes = False
        return 0
    
    def validate_json_schema(self, data:dict) -> bool:
        with open(SCHEMA_PATH, "r") as f:
            schema = json.load(f)
        
        try:
            jsonschema.validate(instance=data, schema=schema)
        except jsonschema.exceptions.ValidationError:
            raise errors.InvalidJsonSchemaException()
        except jsonschema.exceptions.SchemaError:
            raise errors.InvalidJsonSchemaException()

        return True

    def is_json_file(self, filepath:str) -> bool:
        """Validates if the filepath is .json\n
        error handling is left to callee
        
        Params: 
            filename: name to check is a .json file
        Returns:
            True: if file was json format
            False: if file was not json format
        Exceptions:
            None
        """
        # "not not" serves to resolve to true if file was a .json
        return not not re.search('\\.json', filepath, flags=re.IGNORECASE)

    def _parse_uml_data(self, data:dict) -> int:
        """Parses the .json file and populates the classes and relationships.

        Params: 
            data: dict from the loaded .json data.  Should contain the keys 'classes' and 'relationships'.    
        Returns:
            int: 0 if success
        Exceptions:
            None
        """
        uml_classes:list[dict] = data.get("classes")

        if uml_classes is None or not any(uml_classes):
            return -1
        
        self.classes = {c.class_name:c for c in map(self._parse_uml_class, uml_classes)}

        uml_relationships:list[dict] = data.get("relationships")

        self.relationships = set()

        for relation_data in uml_relationships:
            new_relation = self._parse_uml_relationship(relation_data)
            for existing_relation in self.relationships:
                if new_relation.source_class == existing_relation.source_class and new_relation.destination_class == existing_relation.destination_class:
                    raise errors.DuplicateRelationshipException()
            self.relationships.add(new_relation)

    def _parse_uml_class(self, data:dict) -> UmlClass:
        """Converts the provided dict to a UmlClass.

        Params: 
            data: dict representation of the UmlClass.
        Returns:
            UmlClass: an instance of a UmlClass.
        Exceptions:
            None
        """
        def _parse_uml_fields(data:dict) -> UmlField:
            """Converts the provided dict to a Field.
            Params: 
                data: dict representation of the Field.
            Returns:
                Field: an instance of an Field.
            Exceptions:
                None
            """
            if data:
                field = UmlField(data.get("name"), data.get("type"))
                return field

            return None
        
        def _parse_uml_method(data:dict) -> UmlMethod:
            """"""
            def _parse_uml_parameter(data:dict) -> UmlParameter:
                if data:
                    param = UmlParameter(data.get("name"))
                    return param
                
                return None
            
            params:list[UmlParameter] = []
            if data.get("params"):
                params.extend(list(map(_parse_uml_parameter, data.get("params"))))
            return UmlMethod(
                data.get("name"),
                {param.name:param for param in params}
            )

        
        uml_fields:list[UmlField] = []
        if data.get("fields"):
            uml_fields.extend(list(map(_parse_uml_fields, data.get("fields"))))

        uml_methods:list[UmlMethod] = []
        if data.get("methods"):
            uml_methods.extend(list(map(_parse_uml_method, data.get("methods"))))

        methods = {}
        for method in uml_methods:
            if method.name not in methods:
                methods[method.name] = {}
            
            methods[method.name][method.arity] = method

        return UmlClass(
            data.get("name"),
            {field.name:field for field in uml_fields},
            methods
        )

    def _parse_uml_relationship(self, data:dict) -> UmlRelationship:
        """Converts the provided dict to a UmlRelationship.

        Params: 
            data: dict representation of the UmlRelationship.
        Returns:
            UmlRelationship: an instance of an UmlRelationship.
        Exceptions:
            None
        """
        return UmlRelationship(self._relationship_type_from_str(data.get("type")), self.get_umlclass(data.get("source")), self.get_umlclass(data.get("destination")))

    @property
    def _save_object(self) -> dict:
        """Converts the project into a dict in order to save to .json file."""
        return {
            'classes': [c.to_dict() for c in self.classes.values()],
            'relationships': [{
                'source': r.source_class.class_name,
                'destination': r.destination_class.class_name,
                'type': r.relationship_type.name.capitalize()
            } for r in self.relationships]
        }

    def _validate_filepath(self, filepath:str) -> int:
        """Validates the filepath can be used.

        Params: 
            filepath: string for the filepath to validate.
        Returns:
            int: 0 if success
        Exceptions:
            InvalidFileException
        """
        if not os.path.exists(filepath):
            raise errors.InvalidFileException()
        
        if not os.path.isfile(filepath):
            raise errors.InvalidFileException()

        if not self.is_json_file(filepath):
            raise errors.InvalidFileException()

        return 0
    
    def _filepath_exists(self, filepath:str) -> bool:
        """checks if the file exists. WARNING: error raising is left to caller
        Params: 
            filepath: string for the filepath to check existence of.
        Returns:
            True: if file exists
        """
        return os.path.exists(filepath)
    
    def contains_umlclass(self, uml_class_name:str) -> bool:
        """Check if the UmlClass is in the project.
        
        Params: 
            uml_class_name: A string of the class name to look for.
        Returns:
            bool
        Exceptions:
            None
        """
        return uml_class_name in self.classes.keys()
    
    # @_regex_pattern()
    @_has_changed
    def add_umlclass(self, name:str):
        """Adds an UmlClass to the project.

        Params:
            uml_class: The UmlClass instance to add.
        Returns:
            0: if successful
        Exceptions:
            DuplicateClassException
        """
        if name in self.classes:
            raise errors.DuplicateClassException()
        
        errors.valid_name(name)

        self.classes[name] = UmlClass(name, {}, {})
    
    # @_has_changed
    def get_umlclass(self, name:str) -> UmlClass:
        """Gets the UmlClass instance for the provided class name.

        Params:
            name: A string of the class name to provide.
        Returns:
            UmlClass: The instance of the UmlClass or None.
        Exceptions:
            None
        """
        return self.classes.get(name)

    # @_regex_pattern(2)
    @_has_changed
    def rename_umlclass(self,oldName:str, newName:str) -> int:
        """Renames a UmlClass with the first name to the second.

        Params:
            oldName: current name of the class
            newName: new name for the class
        Returns:
            0: if successful
        Exceptions:
            NoSuchObjectException
            DuplicateClassException
        """
        if oldName not in self.classes.keys():
            raise errors.NoSuchObjectException()
        elif newName in self.classes.keys():
            raise errors.DuplicateClassException()
        # rename the class using its own rename method
        uml_class = self.classes.get(oldName)
        uml_class.rename_umlclass(newName)
        uml_class = self.classes.pop(oldName)
        # self.add_umlclass(uml_class)
        
        # rename using the class itself not the copy
        self.classes[newName] = uml_class

        return 0
    
    @_has_changed
    def delete_umlclass(self, name:str) -> int:
        """Deletes a UmlClass with the provided name.

        Params:
            name: current name of the class
        Returns:
            0: if successful
        Exceptions:
            NoSuchObjectException
        """
        uml_class = self.classes.pop(name, None)

        if uml_class:
            # self.delete_relationships(uml_class)
            self.relationships = set(filter(lambda element: element.source_class != uml_class and element.destination_class != uml_class, self.relationships))
            return 0

        raise errors.NoSuchObjectException()

    # @_regex_pattern(count=2)
    @_has_changed
    def add_field(self, classname:str, field_name:str, field_type:str)  -> int:
        """Adds an field to the UmlClass with classname.

        Params:
            classname: current name of the class
            field_name: name of the field to add
        Returns:
            0: if successful
        Exceptions:
            None
        """
        #check if class exists, if so, throw and error
        if self.classes.get(classname).class_fields.get(field_name):
            DuplicateFieldException = errors.DuplicateFieldException()
        #create the field
        self.classes.get(classname).add_field(field_name, field_type)

        return 0

    @_has_changed
    def rename_field(self, classname:str, oldname:str, newname:str) -> int:
        uml_class = self.get_umlclass(classname)

        uml_class.rename_field(oldname, newname)

    @_has_changed
    def delete_field(self, classname:str, fieldname:str) -> int:
        uml_class = self.get_umlclass(classname)

        uml_class.remove_field(fieldname)

    def get_umlmethod(self, classname:str, methodname:str, arity:int) -> UmlMethod:
        uml_class = self.get_umlclass(classname)

        if uml_class and uml_class.class_methods.get(methodname) is None:
            raise errors.MethodNameNotExistsException()
        
        uml_method = uml_class.class_methods.get(methodname).get(arity)

        if uml_method is None:
            raise errors.MethodOverloadNotExistsException()
        
        return uml_method
        

    @_has_changed
    def add_method(self, classname:str, methodname:str, params:list[str]):
        if self.classes.get(classname):
            self.classes.get(classname).add_method(methodname, params)

    @_has_changed
    def rename_method(self, classname:str, oldname:str, newname:str, arity:int):
        if self.classes.get(classname):
            self.classes.get(classname).rename_method(oldname, arity, newname)

    @_has_changed
    def delete_method(self, classname:str, methodname:str, arity:int):
        if self.classes.get(classname):
            self.classes.get(classname).remove_method(methodname, arity)

    @_has_changed
    def add_parameter(self, classname:str, methodname:str, arity:int, parameter:str):
        uml_class = self.get_umlclass(classname)
        uml_class.add_parameter(methodname, arity, parameter)

    @_has_changed
    def rename_parameter(self, classname:str, methodname:str, arity:int, oldname:str, newname:str):
        uml_class = self.get_umlclass(classname)
        uml_class.rename_parameter(methodname, arity, oldname, newname)

    @_has_changed
    def clear_all_parameters(self, classname:str, methodname:str, arity:int):
        """Clears all parameters from a method overload.

        Params:
            classname: current name of the class
            methodname: name of the method
            arity: method overload to operate on
        Returns:
            0: if successful
        Exceptions:
            None
        """
        uml_class = self.get_umlclass(classname)
        uml_class.remove_all_parameters(methodname, arity)
    
    @_has_changed
    def replace_all_parameters(self, classname:str, methodname:str, arity:int, parameters:list[str]):
        """Replace all parameters from a method overload with a new parameter list.

        Params:
            classname: current name of the class
            methodname: name of the method
            arity: method overload to operate on
            parameters: new list of parameter names
        Returns:
            0: if successful
        Exceptions:
            None
        """
        uml_class = self.get_umlclass(classname)
        uml_class.replace_all_parameters(methodname, arity, parameters)

    @_has_changed
    def delete_parameter(self, classname:str, methodname:str, arity:int, parameter:str):
        uml_class = self.get_umlclass(classname)
        uml_class.remove_parameter(methodname, arity, parameter)
    
    def _relationship_type_from_str(self, relationship_str:str)->RelationshipType:
        """Retrieves the relevant value from the RelationshipType Enum based on a string of that value's name or number.
        
        Params:
            relationship_str: the name of the RelationshipType (case-insensitive) or the number of the type as a string.
        
        """
        try:
            return RelationshipType[relationship_str.upper()] # Try to retrieve the type from a name like "DEFAULT"
        except KeyError:
            try:
                return RelationshipType(int(relationship_str)) # Try to retrieve the type from a number string like "0"
            except ValueError:
                raise errors.InvalidRelationshipTypeException()

    def get_relationship(self, source:str, destination:str)->UmlRelationship:
        """Get the relationship between source and destination.

        Params:
            source: name of the source class
            destination: name of the destination class
        Returns:
            0: if successful
        Exceptions:
            NoSuchObjectException
        """
        if source is None or destination is None:
            raise errors.NoSuchObjectException()
        
        if not self.contains_umlclass(source) or not self.contains_umlclass(destination):
            raise errors.NoSuchObjectException()
        
        search_target = UmlRelationship(RelationshipType.DEFAULT, self.get_umlclass(source), self.get_umlclass(destination))
        for relation in self.relationships:
            if search_target.source_class == relation.source_class and search_target.destination_class == relation.destination_class:
                return relation

        raise errors.NoSuchObjectException()

    # @_regex_pattern(2)
    @_has_changed
    def add_relationship(self, source:str, destination:str, relationship_type:str):
        """Creates a relationship of a specified type between the specified classes.
        Params:
            source: name of UML class for source end of the relationship
            destination: name of UML class for destination end of the relationship
        Returns:
            Nothing
        Exceptions:
            UMLException:NullObjectError for nonexistent objects
            UMLException:NoSuchObjectError for nonexistent UMLClass names.
            UMLException:ExistingRelationshipError if a relationship  with the specified source and destination already exists
        """
        if source is None or destination is None:
            raise errors.UMLException("NullObjectError")
        
        if not self.contains_umlclass(source) or not self.contains_umlclass(destination):
            raise errors.UMLException("NoSuchObjectError")
        
        source_class = self.get_umlclass(source)
        destination_class = self.get_umlclass(destination)
        addend = UmlRelationship(self._relationship_type_from_str(relationship_type), source_class, destination_class)

        for relation in self.relationships:
            if addend.destination_class == relation.destination_class and addend.source_class == relation.source_class:
                raise errors.DuplicateRelationshipException()
        
        self.relationships.add(addend)
        
    @_has_changed
    def set_type_relationship(self, source:str, destination:str, new_relationship_type:str):
        """"""
        existing_relation = self.get_relationship(source, destination)
        if existing_relation.relationship_type != self._relationship_type_from_str(new_relationship_type):
            self.relationships.remove(existing_relation)
            existing_relation.relationship_type = self._relationship_type_from_str(new_relationship_type)
            self.relationships.add(existing_relation)
    
    @_has_changed
    def delete_relationship(self, source:str, destination:str):
        """Deletes a relationship of a specified type between the specified classes.
        Params:
            source: name of UML class for source end of the relationship
            destination: name of UML class for destination end of the relationship
        Returns:
            Nothing
        Exceptions:
            UMLException:NullObjectError for nonexistent objects
            UMLException:NoSuchObjectError for nonexistent relationships or UMLClass names.
            ValueError if the relationship isn't found during the remove.
        """
        if source is None or destination is None:
            raise errors.UMLException("NullObjectError")
        
        if not self.contains_umlclass(source) or not self.contains_umlclass(destination):
            raise errors.UMLException("NoSuchObjectError")
        
        match = self.get_relationship(source, destination)

        if not match:
            raise errors.UMLException("NoSuchObjectError") # Note, an error is raised by get_relationship. This should never occur.
        
        self.relationships.remove(match)

class UmlModel():
    """
        Model aspect of the MVC, may not be needed
    """
    