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
from umlclass import UmlClass, Attribute
from umlrelationship import UmlRelationship, RelationshipType

__DIR__ = os.path.dirname(os.path.abspath(__file__))

def is_json_file(filepath:str):
    """Validate if the filepath is .json"""
    return re.search('\\.json', filepath, flags=re.IGNORECASE) is not None

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
        def _parse_uml_attributes(data:dict) -> Attribute:
            """Converts the provided dict to an Attribute.

            Params: 
                data: dict representation of the Attribute.
            Returns:
                Attribute: an instance of an Attribute.
            Exceptions:
                None
            """
            if data:
                attribute = Attribute(data.get("name"))
                # attribute.name = data.get("attr_name")
                return attribute

            return None
        
        uml_attributes:list[Attribute] = []
        if data.get("attributes"):
            uml_attributes.extend(list(map(_parse_uml_attributes, data.get("attributes"))))
        return UmlClass(
            data.get("class_name"),
            {attribute.name:attribute for attribute in uml_attributes}
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

    def save(self) -> int:
        """Saves the currently opened project using the same filepath it was loaded from.

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

    @property
    def _save_object(self) -> dict:
        """Converts the project into a dict in order to save to .json file."""
        return {
            'classes': [{
                'class_name': c.class_name,
                'attributes': [a.to_dict() for a in c.class_attributes.values()]
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

        if not is_json_file(filepath):
            raise errors.InvalidFileException()

        return 0
    
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
    def add_attribute(self, classname:str, attr_name:str)  -> int:
        """Adds an attribute to the UmlClass with classname.

        Params:
            classname: current name of the class
            attr_name: name of the attribute to add
        Returns:
            0: if successful
        Exceptions:
            None
        """
        if self.classes.get(classname):
            self.classes.get(classname).add_attribute(Attribute(attr_name))

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

class UmlApplication:
    """"""
    HELP_PATH = os.path.join(__DIR__, 'help.txt')
    DEFAULT_PROMPT = "BS-uml"

    def __init__(self):
        """"""
        self._current_filepath = None
        self.project:UmlProject = None
        self._command = None
        self._retval = 0
        self.is_running = True
        self.active_class:UmlClass = None

    def _requires_active_project(func):
        """Decorator to validate a project has been loaded.
        
        Exceptions:
            NoActiveProjectException
        """
        @functools.wraps(func)
        def wrapper(self:UmlApplication, *args, **kwargs):
            if self.project is None:
                raise errors.NoActiveProjectException()
            return func(self, *args, **kwargs)
        return wrapper

    def _requires_active_class(func):
        """Decorator to validate a class context exists.
        
        Exceptions:
            NoActiveClassException
        """
        @functools.wraps(func)
        def wrapper(self:UmlApplication, *args, **kwargs):
            if self.active_class is None:
                raise errors.NoActiveClassException()
            return func(self, *args, **kwargs)
        return wrapper

    def _handle_unsaved_changes(func):
        """Decorator to prompt for unsaved changes."""
        @functools.wraps(func)
        def wrapper(self:UmlApplication, *args, **kwargs):
            if self.project and self.project.has_unsaved_changes:
                prompt = "The current project has unsaved changes. Would you like to save before continuing? Y/N. "
                user_response = self.get_user_input(prompt)

                if user_response.lower() == 'y':
                    self.save_project()
                elif user_response.lower() != 'n':
                    print("Invalid input.")
                    return wrapper(self, *args, **kwargs)
            
            return func(self, *args, **kwargs)
        return wrapper

    @property
    def prompt(self) -> str:
        """The CLI prompt to display each loop."""
        if self.active_class:
            return f"{self.DEFAULT_PROMPT}[{self.active_class.class_name}]> "
        return f"{self.DEFAULT_PROMPT}> "
        

    def setup_program(self):
        """Validates requirements for the program are met before attempting to start."""
        if self.project is None:
            self.get_filepath_from_user()
            self.project = UmlProject()
            self.project.load(self._current_filepath)
    
    @_handle_unsaved_changes
    def load_project(self, filepath:str) -> None:
        """Load the project at the provided filepath.

        Params:
            filepath: string
        Returns:
            None
        Exceptions:
            InvalidFileException
        """
        self.project = UmlProject()
        self._retval = self.project.load(filepath)

    @_requires_active_project
    def save_project(self) -> None:
        """Saves the currently opened project using the same filepath it was loaded from.

        Exceptions:
            NoActiveProjectException
        """
        self.project.save()

    @_handle_unsaved_changes
    def new_project(self, filepath:str) -> None:
        """Creates a new project to the provided filepath using the uml project template.
        
        Params:
            filepath: string
        Returns:
            None
        Exceptions:
            InvalidFileException
        """
        if not is_json_file(filepath):
            """"""
            print("Failed: file should be a .json extension.")
            return
        
        template_path = os.path.join(__DIR__, 'templates', 'uml_project_template.json')

        with open(template_path, "r") as t:
            with open(filepath, "w") as f:
                f.write(t.read())

        self.load_project(filepath)

    def inform_invalid_command(self, command:str) -> None:
        """
        enters the terminal into the class context\
        with the specified class name
            Params:   
                command: 
            Returns:
                None
        """
        print(f"Invalid command: {command}.  Use command 'help' for a list of valid commands.")

    def inform_invalid_input(self, user_in:errors.UMLException) -> None:
        """Informs of any other caught UMLExceptions."""
        print(f"Operation failed:UML Error:{user_in}")
    
    def get_filepath_from_user(self) -> None:
        """Get the filepath from the user if they neglected it during load or new."""
        self._current_filepath = input("Filepath: ")
    
    def get_user_input(self, text:str = "") -> str:
        """
        gets user input from the terminal, after prompting with uml name \
        and specified text
            Params:   
                text: the text to prompt the user after the uml name
            Returns:
                the text the user types into the terminal
        """
        user_input = input(f"{self.prompt}{text}")
        while user_input == '':
            user_input = input(f"{self.prompt}{text}")
        return user_input

    def get_user_command(self) -> None:
        """Parses user input and sets the next command to execute."""
        command = self.get_user_input()
        args = command.split()
        cmd = args[0].lower()

        # commands that raise handled exceptions when outside of a class,
        # and function otherwise
        if cmd == 'back':
            self._command = self.command_back

        elif cmd == 'add':
            self._command = self.command_add_umlclass

        elif cmd == 'delete':
            self._command = self.command_delete_umlclass

        elif cmd == 'rename':
            #ask for rest of input
            if len(args) == 1:
                args += self.get_user_input("Enter new class name ").split()
            self._command = lambda: self.command_rename_umlclass(args[1])

        elif cmd == 'attribute':
            self._command = self.command_attribute(args)

        #commands that function differently based on whether in or out of a class
        elif cmd == 'class':
            #ask for rest of input
            if len(args) == 1:
                args += self.get_user_input("Enter class name ").split()
            self._command = lambda: self.command_class(args[1])
            
        elif cmd == 'list':
            self._command = self.command_list

        #commands that function either in or out of a class context
        elif cmd == 'relation':
            self._command = self.command_relation(args)

        elif cmd == 'help':
            self._command = self.command_show_help
        
        elif cmd == 'quit':
            self._command = self.command_quit

        elif cmd == 'save':
            self._command = self.save_project
            
        elif cmd == 'new':
            #ask for rest of input
            if len(args) == 1:
                args += self.get_user_input("Enter new project file name ").split()
            self._command = lambda: self.new_project(args[1])
            
        elif cmd == 'load':
            #ask for rest of input
            if len(args) == 1:
                args += self.get_user_input("Enter project file name ").split()
            self._command = lambda: self.load_project(args[1])
        
        # now catches all cases
        else:
            self._command = lambda: self.inform_invalid_command(command)

    # APPLICATION COMMANDS

    def command_show_help(self):
        """Command: help  
        Displays help menu.
        """
        with open(self.HELP_PATH, "r") as f:
            print(f.read())

    @_handle_unsaved_changes
    def command_quit(self):
        """Quits the program.  Prompts the user if there are unsaved changes."""
        # Check if file is unsaved and prompt user to save or discard
        # Above comment is handled by the decorator @_handle_unsaved_changes

        # Exit the program
        self.is_running = False

    def command_back(self) -> None:
        """Brings terminal out of class context"""
        if self.active_class:
            self.active_class = None

    @_requires_active_project
    def command_list(self) -> None:
        """
        Displays list of classes when out of class context,
        and displays class contents when in a class

        Exceptions:
            NoActiveProjectException
        """
        if not self.active_class:
            self._render_umlproject()
        else:
            self._render_umlclass(self.active_class)

    @_requires_active_project
    def command_class(self, name:str) -> None:
        """enters the terminal into the class context with the specified class name

        Params:   
            name: the name of the class to enter the context of
        Exceptions:
            NoActiveProjectException
        """
        if self.active_class and self.active_class.class_name == name:
            return
        
        self.active_class = self.project.get_umlclass(name)

        if not self.active_class:
            errors.valid_name(name)
            self.active_class = UmlClass(name, {})
    
    @_requires_active_class
    def command_add_umlclass(self) -> None:
        """adds the class the context is in to the project
        
        Exceptions:
            NoActiveClassException
        """
        self.project.add_umlclass(self.active_class)

    @_requires_active_class
    def command_delete_umlclass(self):
        """Removes the UmlClass in the current context from the project.
        Prompts and informs the user to delete relationships.
        
        Exceptions:
            NoActiveClassException
        """        
        # Confirm with user
        prompt = "Deleting a class will also remove its relationships. Y/N to continue. "
        user_response = self.get_user_input(prompt)
        if user_response.lower() == "n":
            return
        if user_response.lower() != "y":
            print("Invalid input.")
            return self.command_delete_umlclass()
        # Remove from project
        self.project.delete_umlclass(self.active_class.class_name)
        self.active_class = self.project.get_umlclass(self.active_class.class_name)

    @_requires_active_class
    def command_rename_umlclass(self, name:str):
        """Renames the UmlClass in the current context.
        
        Params:
            name: the new name for the class.
        Exceptions:
            NoActiveClassException
        """
        self.project.rename_umlclass(self.active_class.class_name, name)
        self.active_class = self.project.get_umlclass(name)

    @_requires_active_class
    def command_attribute(self, args:list[str]):
        """Parses additional args for attribute commands.
        
        Params:
            args: string list of additional args
        Exceptions:
            NoActiveClassException
        """
        if len(args) < 3:
            return lambda: self.inform_invalid_command(" ".join(args))

        cmd = args[1].lower()
        
        if cmd == 'add':
            return lambda: self.command_add_attribute(args[2])
        elif cmd == 'delete':
            return lambda: self.command_delete_attribute(args[2])
        elif cmd == 'rename':
            return lambda: self.command_rename_attribute(args[2], args[3])

        return lambda: self.inform_invalid_command(" ".join(args))

    @_requires_active_class
    def command_add_attribute(self, name:str) -> None:
        """Adds an attribute to the UmlClass in current context.
        
        Exceptions:
            NoActiveClassException
        """
        self.active_class.add_attribute(Attribute(name))

    @_requires_active_class
    def command_delete_attribute(self, name:str) -> None:
        """Deletes an attribute from the UmlClass in the current context.
        
        Exceptions:
            NoActiveClassException
        """
        self.active_class.remove_attribute(name)

    @_requires_active_class
    def command_rename_attribute(self, oldname:str, newname:str) -> None:
        """Renames an attribute from the UmlClass in the current context.
        
        Params:
            oldname: the current name of the attribute to rename
            newname: the name to change the attribute to
        Exceptions:
            NoActiveClassException
            InvalidNameError
            DuplicateNameError
        """
        self.active_class.rename_attribute(oldname, newname)

    @_requires_active_project
    def command_relation(self, args:list[str]):
        """Parses additional args for relation commands.
        
        Params:
            args: string list of additional args
        Exceptions:
            NoActiveProjectException
        """
        if len(args) < 2:
            return lambda: self.inform_invalid_command(" ".join(args))
        
        cmd = args[1].lower()

        if cmd == 'add':
            return lambda: self.command_add_relation(args[2], args[3])
        elif cmd == 'delete':
            return lambda: self.command_delete_relation(args[2], args[3])
        elif cmd == 'list':
            return self.command_list_relation
        return lambda: self.inform_invalid_command(" ".join(args))

    @_requires_active_project
    def command_add_relation(self, source:str, destination:str) -> None:
        """Adds a relationship.
        
        Params:
            source: a class name owning the source
            destination: a class name owning the destination
        Exceptions:
            NoActiveProjectException
            NoSuchObjectError
        """
        self.project.add_relationship(source, destination)

    @_requires_active_project
    def command_delete_relation(self, source:str, destination:str) -> None:
        """Delete a relationship.
        
        Params:
            source: a class name owning the source
            destination: a class name owning the destination
        Exceptions:
            NoActiveProjectException
            NoSuchObjectError
        """
        self.project.delete_relationship(source, destination)

    @_requires_active_project
    def command_list_relation(self):
        """Display all relationships."""
        if len(self.project.relationships) == 0:
            print("No relationships to display")
        else:
            print("Displaying", len(self.project.relationships), "relationships.")
            print("\n".join(map(str, self.project.relationships)))

    def run(self):
        """
        runs the program until user exit
            Params:   
                None
            Returns:
                0 if program exited successfully
        """
        while self.is_running:
            try:
                if self._command is None:
                    self.get_user_command()
                self._command()
            except errors.NoActiveProjectException:
                print("No project has been loaded. Use command: load <filepath> or new <filepath> to get started.")
            except errors.NoActiveClassException:
                print("No active class selection. Use command: class <class name> to select a class.")
            except errors.DuplicateClassException:
                print("Failed: An class with that name already exists in this project.")
            except errors.DuplicateAttributeException:
                print("Failed: An attribute with that name already exists on this class.")
            except errors.InvalidFileException:
                print("Invalid file: Use command: new <filename.json> to make a new file, \
                    \n or command: load <filename.json> to load a file that exists \
                    \n in current folder, or specify subfolder with <filepath/filename.json>")
            except errors.DuplicateRelationshipException:
                print("Failed: This relationship already exists in this project.")
            except errors.UMLException as uml_e:
                self.inform_invalid_input(uml_e)
            except EOFError:
                self.is_running = False
            except Exception as e:
                self.inform_invalid_input(e)
                logging.info(f" unknown error occured: {e.args}")
            finally:
                self._command = None
        return 0
    
    def _render_umlclass(self, uml_class:UmlClass):
        """Display a UmlClass."""
        def calc_spaces(s:str, l:int) -> str:
            size_delta = abs(len(s) - l)

            if not size_delta:
                return f"{s} "
            
            if not size_delta % 2:
                return s + " " * size_delta
            # print(s)
            # return s
            return s + " " * (size_delta + 1)
            
        header = uml_class.class_name
        body = []

        longest_word_length = len(header)
        for k, v in uml_class.class_attributes.items():
            body.append(k)
            if len(k) > longest_word_length:
                longest_word_length = len(k)
        
        sep = "+-" + "-" * longest_word_length + "-+"
        output = sep
        output += "\n|" + calc_spaces(header, longest_word_length) + "|"
        output += "\n" + sep
        for s in body:
            output += "\n|-" + calc_spaces(s, longest_word_length) + "|"
        output += "\n" + sep
        
        print(output)

    def _render_umlproject(self) -> None:
        """Display a UmlProject."""
        if any(self.project.classes):
            print(f"Displaying {len(self.project.classes)} classes.")
            for c in self.project.classes.values():
                self._render_umlclass(c)
        else:
            print("No classes to display.")

def main():
    """Entry point for the program."""
    app = UmlApplication()
    app.run()

if __name__ == "__main__":
    main()