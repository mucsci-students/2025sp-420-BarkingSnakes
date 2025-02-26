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

import errors
from umlclass import UmlClass, UmlField
from umlrelationship import UmlRelationship, RelationshipType

#project directory path
__DIR__ = os.path.dirname(os.path.abspath(__file__))

class UmlProject:
    """"""
    def __init__(self):
        self.classes:dict[str,UmlClass] = {}
        self.relationships:set[UmlRelationship] = set()
        self._save_path = None
        self.has_unsaved_changes = False

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
        
        self._save_path = filepath

        with open(filepath, "r") as f:
            data =  json.load(f)
            self._parse_uml_data(data)

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
        with open(self._save_path, "w") as f:
            json.dump(self._save_object, f, indent=4)

        self.has_unsaved_changes = False
        return 0
    
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

        if uml_classes is None:
            return -1
        
        self.classes = {c.class_name:c for c in map(self._parse_uml_class, uml_classes)}

        uml_relationships:list[dict] = data.get("relationships")

        self.relationships = set([self._parse_uml_relationship(r) for r in uml_relationships])

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
                field = UmlField(data.get("name"))
                return field

            return None
        
        uml_fields:list[UmlField] = []
        if data.get("fields"):
            uml_fields.extend(list(map(_parse_uml_fields, data.get("fields"))))
        return UmlClass(
            data.get("class_name"),
            {field.name:field for field in uml_fields}
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
        return UmlRelationship(RelationshipType.DEFAULT, self.get_umlclass(data.get("source")), self.get_umlclass(data.get("destination")))

    @property
    def _save_object(self) -> dict:
        """Converts the project into a dict in order to save to .json file."""
        return {
            'classes': [{
                'class_name': c.class_name,
                'fields': [f.to_dict() for f in c.class_fields.values()]
            } for c in self.classes.values()],
            'relationships': [{
                'source': r.source_class.class_name,
                'destination': r.destination_class.class_name
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
    
    @_has_changed
    def add_umlclass(self, uml_class:UmlClass):
        """Adds an UmlClass to the project.

        Params:
            uml_class: The UmlClass instance to add.
        Returns:
            0: if successful
        Exceptions:
            DuplicateClassException
        """
        if uml_class.class_name in self.classes:
            raise errors.DuplicateClassException()
        self.classes[uml_class.class_name] = uml_class
    
    @_has_changed
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
        uml_class = self.classes.pop(oldName)
        uml_class.rename_umlclass(newName)
        self.add_umlclass(uml_class)
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

    @_has_changed
    def add_field(self, classname:str, field_name:str)  -> int:
        """Adds an field to the UmlClass with classname.

        Params:
            classname: current name of the class
            field_name: name of the field to add
        Returns:
            0: if successful
        Exceptions:
            None
        """
        if self.classes.get(classname):
            self.classes.get(classname).add_field(UmlField(field_name))

    def get_relationship(self, source:str, destination:str, relationship_type:RelationshipType = RelationshipType.DEFAULT)->UmlRelationship:
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
        
        search_target = UmlRelationship(relationship_type, self.get_umlclass(source), self.get_umlclass(destination))
        for relation in self.relationships:
            if search_target == relation:
                return relation

        raise errors.NoSuchObjectException()

    @_has_changed
    def add_relationship(self, source:str, destination:str, relationship_type:RelationshipType = RelationshipType.DEFAULT):
        """Creates a relationship of a specified type between the specified classes.
        Params:
            source: name of UML class for source end of the relationship
            destination: name of UML class for destination end of the relationship
            relationship_type: the type of relationship, default value: DEFAULT
        Returns:
            Nothing
        Exceptions:
            UMLException:NullObjectError for nonexistent objects
            UMLException:NoSuchObjectError for nonexistent UMLClass names.
            UMLException:ExistingRelationshipError if the relationship already exists
        """
        if source is None or destination is None:
            raise errors.UMLException("NullObjectError")
        
        if not self.contains_umlclass(source) or not self.contains_umlclass(destination):
            raise errors.UMLException("NoSuchObjectError")
        
        source_class = self.get_umlclass(source)
        destination_class = self.get_umlclass(destination)
        addend = UmlRelationship(relationship_type, source_class, destination_class)

        if addend in self.relationships:
            raise errors.DuplicateRelationshipException()
        
        self.relationships.add(addend)
        
    @_has_changed
    def delete_relationship(self, source:str, destination:str, relationship_type:RelationshipType = RelationshipType.DEFAULT):
        """Deletes a relationship of a specified type between the specified classes.
        Params:
            source: name of UML class for source end of the relationship
            destination: name of UML class for destination end of the relationship
            relationship_type: the type of relationship, default value: DEFAULT
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
        
        match = self.get_relationship(source, destination, relationship_type)

        if not match:
            raise errors.UMLException("NoSuchObjectError") # Note, an error is raised by get_relationship. This should never occur.
        
        self.relationships.remove(match)

class UmlModel():
    """
        Model aspect of the MVC, may not be needed
    """
    