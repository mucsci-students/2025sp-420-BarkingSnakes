# Filename: umlmodel.py
# Authors: Steven Barnes, John Hershey, Evan Magill, Kyle Kalbach, Spencer Hoover, Juliana Vinluan
# Last Edit Date: 2025-05-12
# Description: Model for the Uml editor program.

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
from abc import ABC, abstractmethod
from datetime import datetime

# project directory path
__DIR__ = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(__DIR__, "templates", "umlschema.json")
REGEX_DEFAULT = "^[A-Za-z][A-Za-z0-9_]*$"


class UmlProject:
    """"""

    def __init__(self):
        self.classes: dict[str, UmlClass] = {}
        self.relationships: set[UmlRelationship] = set()
        self._save_path = None
        self.has_unsaved_changes = False

    def _has_changed(func):
        @functools.wraps(func)
        def wrapper(self: UmlProject, *args, **kwargs):
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
        template_path = os.path.join(__DIR__, "templates", "uml_project_template.json")
        # open needs moved to save section in model
        with open(template_path, "r") as t:
            data = json.load(t)
            self.validate_json_schema(data)
            self._parse_uml_data(data)

    def load(self, filepath: str) -> int:
        """Load the project at the provided filepath.

        Params:
            filepath: string
        Returns:
            int: 0 if success
        Exceptions:
            InvalidFileException
            InvalidJsonSchemaException
        """
        #method returns 0 when true, which is equivalent to false
        #if not 0 errors should be called in validate
        self._validate_filepath(filepath)    
        with open(filepath, "r") as f:
            # if file invalid raise catch error and raise schema one
            try:
                data =  json.load(f)
            except:
                raise errors.InvalidJsonSchemaException()
            self.validate_json_schema(data)
            self._parse_uml_data(data)
        # use when saving later
        # use command to ensure the save path is only set to valid files
        self.set_save_path(filepath)

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
        # this shouldn't be called since the save path should only be set 
        # by its setter method that should already do this, 
        # but in case it's still set manually, save checks that the path is valid
        self._is_json_file(self._save_path)
        self.validate_json_schema(self._save_object)
        # will override, handled by caller(umlapplication)
        with open(self._save_path, "w") as f:
            json.dump(self._save_object, f, indent=4)
        self.has_unsaved_changes = False
        return 0
    
    def set_save_path(self, filepath: str):
        """sets the model's save path, as long as it is a valid file"""
        # make sure the filepath is valid before setting it 
        # so that it cant be set to an invalid file type
        # but only if a type was specifed
        if filepath:
            self._is_json_file(filepath)
        self._save_path = filepath

    def _is_json_file(self, filepath: str) -> bool:
        """Validates if the filepath is .json\n

        Params:
            filename: name to check is a .json file
        Returns:
            None
        Exceptions:
            InvalidFileException: if the file was not a .json type
        """
        
        if not filepath.endswith(".json"):#bool(re.search('\\.json', filepath, flags=re.IGNORECASE)):
            raise errors.InvalidFileException("not a json file")

    def validate_json_schema(self, data: dict) -> bool:
        "verifies that the given dict matches the project template"
        with open(SCHEMA_PATH, "r") as f:
            schema = json.load(f)

        try:
            validator = jsonschema.Draft7Validator(schema)
            validator.validate(instance=data)
        # this is only raised if our schema template is invalid, so handling is unset currently
        #except jsonschema.exceptions.SchemaError:
        #    raise errors.NoSuchErrorException()
        except jsonschema.exceptions.ValidationError:
            raise errors.InvalidJsonSchemaException()
        return True

    # parsing methods
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
        uml_relationships:list[dict] = data.get("relationships")

        if uml_classes is None or uml_relationships is None:
            raise errors.InvalidJsonSchemaException()
        
        if self._has_duplicate_objects(uml_classes):
            raise errors.InvalidJsonSchemaException()
        
        self.classes = {c.class_name:c for c in map(self._parse_uml_class, uml_classes)}

        self.relationships = set()

        for relation_data in uml_relationships:
            new_relation = self._parse_uml_relationship(relation_data)
            for existing_relation in self.relationships:
                if new_relation.source_class == existing_relation.source_class and new_relation.destination_class == existing_relation.destination_class:
                    raise errors.InvalidJsonSchemaException()
                    #raise errors.DuplicateRelationshipException()
            self.relationships.add(new_relation)

    def _parse_uml_class(self, data: dict) -> UmlClass:
        """Converts the provided dict to a UmlClass.

        Params:
            data: dict representation of the UmlClass.
        Returns:
            UmlClass: an instance of a UmlClass.
        Exceptions:
            None
        """

        def _parse_uml_fields(data: dict) -> UmlField:
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
            raise errors.InvalidJsonSchemaException()

        def _parse_uml_method(data: dict) -> UmlMethod:
            """"""

            def _parse_uml_parameter(data: dict) -> UmlParameter:
                if data:
                    param = UmlParameter(data.get("name"), data.get("type"))
                    return param
                raise errors.InvalidJsonSchemaException()

            params: list[UmlParameter] = []
            if data.get("params"):
                params.extend(list(map(_parse_uml_parameter, data.get("params"))))
            return UmlMethod(
                data.get("name"),
                data.get("return_type"),
                params
            )
        def _parse_uml_position(data:dict) -> tuple[float,float]:
            """parses the position of the class"""
            if data:
                return data.get("x", 0), data.get("y", 0)
            return 0, 0
        
        uml_fields: list[UmlField] = []
        if data.get("fields"):
            uml_fields.extend(list(map(_parse_uml_fields, data.get("fields"))))
            #check for dupes
            if self._has_duplicate_objects(data.get("fields")):
                raise errors.InvalidJsonSchemaException()
        
        uml_methods:list[UmlMethod] = []
        if data.get("methods"):
            uml_methods.extend(list(map(_parse_uml_method, data.get("methods"))))
            #check for dupes
            # if self._has_duplicate_objects(data.get("methods")):
            #     raise errors.InvalidJsonSchemaException()
        
        methods = {}
        for method in uml_methods:
            if method.name not in methods:
                methods[method.name] = {}
            
            methods[method.name][method.overloadID] = method

        # gets the position
        position = _parse_uml_position(data.get("position"))
        return UmlClass(
            data.get("name"),
            {field.name: field for field in uml_fields},
            methods,
            position[0],
            position[1]
        )

    def _parse_uml_relationship(self, data: dict) -> UmlRelationship:
        """Converts the provided dict to a UmlRelationship.

        Params:
            data: dict representation of the UmlRelationship.
        Returns:
            UmlRelationship: an instance of an UmlRelationship.
        Exceptions:
            None
        """
        try:
            return UmlRelationship(self._relationship_type_from_str(data.get("type"))\
            , self.get_umlclass(data.get("source")), self.get_umlclass(data.get("destination")))
        except errors.NoSuchObjectException as e:
            raise errors.InvalidJsonSchemaException()

    # schema methods
    def _has_duplicate_objects(self, data:list[dict]) -> bool:
        """checks if the given list of dicts has any duplicate names
        
        Params: 
            data: list of dicts to check for dupes
        Returns:
            False: if no duplicates were in list
            True: if a duplicate name was detected
        Exceptions:
            None
        """
        # make a list of every "name" in each dict in the list
        nameList = [(obj["name"] if "name" in obj else "") for obj in data]
        # convert the name list to a set to remove duplicate names 
        # and compare lengths: if different then a dupe was removed
        return len(set(nameList)) != len(data)
    
    @property
    def _save_object(self) -> dict:
        """Converts the project into a dict in order to save to .json file."""
        return {
            "classes": [c.to_dict() for c in self.classes.values()],
            "relationships": [
                {
                    "source": r.source_class.class_name,
                    "destination": r.destination_class.class_name,
                    "type": r.relationship_type.name.capitalize(),
                }
                for r in self.relationships
            ],
        }

    def _validate_filepath(self, filepath: str) -> int:
        """Validates the filepath can be used.

        Params:
            filepath: string for the filepath to validate.
        Returns:
            int: 0 if success
        Exceptions:
            InvalidFileException
        """
        if not self._filepath_exists(filepath):
            raise errors.InvalidFileException("does not exist")

        if not os.path.isfile(filepath):
            raise errors.InvalidFileException("not a file")
        #this now raises an error on its own if the file given wasn't a json file
        self._is_json_file(filepath)

        return 0

    def _filepath_exists(self, filepath: str) -> bool:
        """checks if the file exists. WARNING: error raising is left to caller
        Params:
            filepath: string for the filepath to check existence of.
        Returns:
            True: if file exists
        """
        return os.path.exists(filepath)
    
    #class methods
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

    @_has_changed
    def add_umlclass(self, name: str):
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
    def get_umlclass(self, name: str) -> UmlClass:
        """Gets the UmlClass instance for the provided class name.

        Params:
            name: A string of the class name to provide.
        Returns:
            UmlClass: The instance of the UmlClass or None.
        Exceptions:
            NoSuchClassException
        """
        if self.classes.get(name):
            return self.classes.get(name)
        #if the class didn't exist raise an error
        raise errors.NoSuchObjectException()

    @_has_changed
    def rename_umlclass(self, oldName: str, newName: str) -> int:
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
    def delete_umlclass(self, name: str) -> int:
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
            self.relationships = set(
                filter(
                    lambda element: element.source_class != uml_class
                    and element.destination_class != uml_class,
                    self.relationships,
                )
            )
            return 0

        raise errors.NoSuchObjectException()

    @_has_changed
    def update_position_umlclass(self,name:str, x_pos:float, y_pos:float):
        """updates a umlclass's position in the model

        Params:
            name: name of the class to update position
            x_pos: new x(left-right) position of the class
            y_pos: new y(left-right) position of the class
        Returns:
            None
        Exceptions:
            NoSuchObjectException
        """
        if name not in self.classes.keys():
            raise errors.NoSuchObjectException()
        # update the pos using the class method
        self.get_umlclass(name).set_umlclass_position(x_pos, y_pos)
        
    def get_position_umlclass(self,name:str) -> tuple[float, float]:
        """gets a uml classes position

        Params:
            name: name of the class to update position
        Returns:
            tuple(float, float): x and y position of the class
        Exceptions:
            NoSuchObjectException
        """
        if name not in self.classes.keys():
            raise errors.NoSuchObjectException()
        # return the pos using the class's method
        return self.get_umlclass(name).get_umlclass_position()
    
    #field methods
    @_has_changed
    def add_field(self, classname: str, field_name: str, field_type: str) -> int:
        """Adds an field to the UmlClass with classname.

        Params:
            classname: current name of the class
            field_name: name of the field to add
        Returns:
            0: if successful
        Exceptions:
            DuplicateFieldException
        """
        # check if field exists, if so, throw an error
        if self.classes.get(classname).class_fields.get(field_name):
            raise errors.DuplicateFieldException()
        #create the field
        self.classes.get(classname).add_field(field_name, field_type)

        return 0

    @_has_changed
    def rename_field(self, classname: str, oldname: str, newname: str):
        uml_class = self.get_umlclass(classname)

        uml_class.rename_field(oldname, newname)
        
    @_has_changed
    def change_field_type(self, classname: str, fieldname: str, newtype: str):
        """changes the type of the field with name field name"""
        uml_class = self.get_umlclass(classname)

        uml_class.change_field_type(fieldname, newtype)

    @_has_changed
    def delete_field(self, classname: str, fieldname: str) -> int:
        uml_class = self.get_umlclass(classname)

        uml_class.remove_field(fieldname)

    # method methods
    def get_umlmethod(self, classname:str, methodname:str, overload_id:str) -> UmlMethod:
        uml_class = self.get_umlclass(classname)

        if uml_class and uml_class.class_methods.get(methodname) is None:
            raise errors.MethodNameNotExistsException()
        
        uml_method = uml_class.class_methods.get(methodname).get(overload_id)

        if uml_method is None:
            raise errors.MethodOverloadNotExistsException()

        return uml_method

    @_has_changed
    def add_method(self, classname:str, methodname:str, return_type:str, params:list[tuple[str, str]]):
        if self.classes.get(classname):
            self.classes.get(classname).add_method(methodname, return_type, params)

    @_has_changed
    def rename_method(self, classname:str, oldname:str, newname:str, overload_id:str):
        if self.classes.get(classname):
            self.classes.get(classname).rename_method(oldname, overload_id, newname)
    
    @_has_changed
    def change_method_type(self, classname:str, name:str, newtype:str, overload_id:str):
        """changes the method type"""
        uml_class = self.classes.get(classname)
        uml_class.change_method_type(name, overload_id, newtype)

    @_has_changed
    def delete_method(self, classname:str, methodname:str, overload_id:str):
        if self.classes.get(classname):
            self.classes.get(classname).remove_method(methodname, overload_id)

    # parameter methods
    @_has_changed
    def add_parameter(self, classname:str, methodname:str, overload_id:str, parameter:str, param_type:str):
        uml_class = self.get_umlclass(classname)
        uml_class.add_parameter(methodname, overload_id, parameter, param_type)

    @_has_changed
    def rename_parameter(self, classname:str, methodname:str, overload_id:str, oldname:str, newname:str):
        uml_class = self.get_umlclass(classname)
        uml_class.rename_parameter(methodname, overload_id, oldname, newname)

    @_has_changed
    def clear_all_parameters(self, classname:str, methodname:str, overload_id:str):
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
        uml_class.remove_all_parameters(methodname, overload_id)
    
    @_has_changed
    def replace_all_parameters(self, classname:str, methodname:str, overload_id:str, parameters:list[tuple[str, str]]):
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
        uml_class.replace_all_parameters(methodname, overload_id, parameters)

    @_has_changed
    def delete_parameter(self, classname:str, methodname:str, overload_id:str, parameter:str):
        uml_class = self.get_umlclass(classname)
        uml_class.remove_parameter(methodname, overload_id, parameter)
    
    # relationship methods
    def _relationship_type_from_str(self, relationship_str:str)->RelationshipType:
        """Retrieves the relevant value from the RelationshipType Enum based on a string of that value's name or number.

        Params:
            relationship_str: the name of the RelationshipType (case-insensitive) or the number of the type as a string.

        """
        if not relationship_str:
            raise errors.NullObjectException()
        relation_type = None
        try:
            # Try to retrieve the type from a name like "AGGREGATION"
            relation_type = RelationshipType[relationship_str.upper()]
        except KeyError:
            try:
                # Try to retrieve the type from a number string like "0"
                relation_type = RelationshipType(int(relationship_str))
            except ValueError:
                raise errors.InvalidRelationshipTypeException()
        if relation_type.value == 0:
            raise errors.InvalidRelationshipTypeException()
        return relation_type

    def get_relationship(self, source: str, destination: str) -> UmlRelationship:
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
            raise errors.NullObjectException()
        
        if not self.contains_umlclass(source) or not self.contains_umlclass(destination):
            raise errors.NoSuchObjectException()

        search_target = UmlRelationship(
            RelationshipType.DEFAULT,
            self.get_umlclass(source),
            self.get_umlclass(destination),
        )
        for relation in self.relationships:
            if (
                search_target.source_class == relation.source_class
                and search_target.destination_class == relation.destination_class
            ):
                return relation

        raise errors.NoSuchObjectException()

    @_has_changed
    def add_relationship(self, source: str, destination: str, relationship_type: str):
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
        if source is None or destination is None or relationship_type is None:
            raise errors.NullObjectException()

        if not self.contains_umlclass(source) or not self.contains_umlclass(
            destination
        ):
            raise errors.NoSuchObjectException()

        source_class = self.get_umlclass(source)
        destination_class = self.get_umlclass(destination)
        addend = UmlRelationship(
            self._relationship_type_from_str(relationship_type),
            source_class,
            destination_class,
        )

        for relation in self.relationships:
            if (
                addend.destination_class == relation.destination_class
                and addend.source_class == relation.source_class
            ):
                raise errors.DuplicateRelationshipException()

        self.relationships.add(addend)

    @_has_changed
    def set_type_relationship(self, source:str, destination:str, new_relationship_type:str):
        """sets the type of an existing relation
        Params:
            source: name of UML class for source end of the relationship
            destination: name of UML class for destination end of the relationship
            new_relationship_type: the type to change the relation to
        Returns:
            None
        Exceptions:
            UMLException: 
        """
        existing_relation = self.get_relationship(source, destination)
        if existing_relation.relationship_type != self._relationship_type_from_str(
            new_relationship_type
        ):
            self.relationships.remove(existing_relation)
            existing_relation.relationship_type = self._relationship_type_from_str(
                new_relationship_type
            )
            self.relationships.add(existing_relation)

    @_has_changed
    def delete_relationship(self, source:str, destination:str):
        """Deletes a relationship between the specified classes.
        Params:
            source: name of UML class for source end of the relationship
            destination: name of UML class for destination end of the relationship
        Returns:
            None
        Exceptions:
            UMLException:NullObjectError if src or dest is None
            UMLException:NoSuchObjectError for nonexistent relationships or UMLClasses.
        """
        if source is None or destination is None:
            raise errors.NullObjectException()
        
        if not self.contains_umlclass(source):
            # text added so later sprint can more clearly specify what doesn't exist
            raise errors.NoSuchObjectException("class",source)
        elif not self.contains_umlclass(destination):
            raise errors.NoSuchObjectException("class",destination)
        
        # if relation does not exist get_relationship will raise an error
        match = self.get_relationship(source, destination)
        
        self.relationships.remove(match)

    def _save_memento(self) -> Memento:
        """Returns a Concrete Memento that captures the current state."""
        return ConcreteMemento(self._save_object)

    @_has_changed
    def _restore_memento(self, memento: Memento) -> None:
        """Sets the current state to the State captured in the memento."""
        self._parse_uml_data(memento.get_state())

    def _validate_memento(self, memento: Memento) -> bool:
        """Returns True if a memento has a valid state."""
        return self.validate_json_schema(memento.get_state())


class Memento(ABC):
    """Encapsulating interface that only allows access to the creation date of the memento."""

    @abstractmethod
    def get_date(self) -> datetime:
        """Returns the creation date and time of the memento."""

class ConcreteMemento(Memento):
    """Implementation of the memento interface that stores a state accessible to the originator object."""

    def __init__(self, state: dict) -> None:
        self._state = state
        self._date = datetime.now()

    def get_state(self) -> dict:
        """Returns the state of the Concrete Memento"""
        return self._state

    def get_date(self):
        """returns the creation date and time of the Concrete Memento"""
        return self._date

class Caretaker:
    """Class for keeping track of mementos and the redo stack and the originator."""

    def __init__(self, originator: UmlProject) -> None:
        self._undo_stack = []
        self._redo_stack = []
        self._originator = originator
        self._current_memento = self._originator._save_memento()

    def backup(self) -> None:
        """Requests the originator to save the current state and stores the returned memento wiping the redo stack."""
        self._undo_stack.append(self._current_memento)
        self._current_memento = self._originator._save_memento()
        self._redo_stack = []

    def undo(self) -> None:
        """Returns the origintor to the previous state."""
        if len(self._undo_stack):
            memento = self._undo_stack.pop()

            self._originator._restore_memento(memento)
            self._redo_stack.append(self._current_memento)
            self._current_memento = memento
        else:
            raise errors.NoActionsLeftException()
            

    def redo(self) -> None:
        """Returns the state to a previously undon state."""
        if len(self._redo_stack):
            # Checks redo stack is not empty
            memento = self._redo_stack.pop()

            # Restore to memento from _redo_stack
            self._originator._restore_memento(memento)
            # Move current state onto memento stack
            self._undo_stack.append(self._current_memento)
            # Set the _current_memento to the new current memento
            self._current_memento = memento
        else:
            raise errors.NoActionsLeftException()