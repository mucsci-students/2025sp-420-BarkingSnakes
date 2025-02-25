# Filename: uml.py
# Authors: Steven Barnes, John Hershey, Evan Magill, Kyle Kalbach
# Date: 2025-02-24
# Description: Controller for the UML
import os
import functools
import logging

from uml import UmlProject
from umlclass import UmlClass, UmlField
import errors
import uml
class UmlApplication:()

class UmlApplication:
    """Application controller for the UML"""
    HELP_PATH = os.path.join(uml.__DIR__, 'help.txt')
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
        # currently, instead of passing the filename, the command
        # section adds the filename to the project first before calling this
        self.project.save()

    #change project for later tasks
    @_handle_unsaved_changes
    def new_project(self) -> None:
        """Creates a new project using the uml project template.
        
        Params:
            None
        Returns:
            None
        """
        #declare new project, and call "new" method
        self.project = UmlProject()
        self.project.new()

    @_handle_unsaved_changes
    def new_project(self, filepath:str) -> None:
        """Creates a new project using the uml project template,
            and stores a filename.
        
        Params:
            filepath: string to be stored for address to save to
        Returns:
            None
        Exceptions:
            InvalidFileException
        """
        if not UmlProject.is_json_file(self, filepath):
            raise errors.InvalidFileException()
        self.new_project()
        
    
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

    #might move to view
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

        elif cmd == 'field':
            self._command = self.command_field(args)

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
            # if no filename specified and no current save path, then ask
            if len(args) == 1 and not self.project._save_path:
                filename = self.get_user_input("Enter file name")
                #validate filename as json and set it
                self.project.is_json_file(filename)
                self.project._save_path = filename
            
            self._command = self.save_project()
            
        elif cmd == 'new':
            # if only new is specified, then 
            # assume file will be provided at save
            if len(args) == 1:
                self._command = lambda: self.new_project()
            # if filename is provided, then take it, but
            # don't use to create file at this time
            else:   
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
    def command_field(self, args:list[str]):
        """Parses additional args for field commands.
        
        Params:
            args: string list of additional args
        Exceptions:
            NoActiveClassException
        """
        if len(args) < 3:
            return lambda: self.inform_invalid_command(" ".join(args))

        cmd = args[1].lower()
        
        if cmd == 'add':
            return lambda: self.command_add_field(args[2])
        elif cmd == 'delete':
            return lambda: self.command_delete_field(args[2])
        elif cmd == 'rename':
            return lambda: self.command_rename_field(args[2], args[3])

        return lambda: self.inform_invalid_command(" ".join(args))

    @_requires_active_class
    def command_add_field(self, name:str) -> None:
        """Adds an field to the UmlClass in current context.
        
        Exceptions:
            NoActiveClassException
        """
        self.active_class.add_field(name)

    @_requires_active_class
    def command_delete_field(self, name:str) -> None:
        """Deletes an field from the UmlClass in the current context.
        
        Exceptions:
            NoActiveClassException
        """
        self.active_class.remove_field(name)

    @_requires_active_class
    def command_rename_field(self, oldname:str, newname:str) -> None:
        """Renames an field from the UmlClass in the current context.
        
        Params:
            oldname: the current name of the field to rename
            newname: the name to change the field to
        Exceptions:
            NoActiveClassException
            InvalidNameError
            DuplicateNameError
        """
        self.active_class.rename_field(oldname, newname)

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
        self.new_project()
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
            except errors.DuplicateFieldException:
                print("Failed: An field with that name already exists on this class.")
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
        for k, v in uml_class.class_fields.items():
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