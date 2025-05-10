# Filename: umlcontroller.py
# Authors: Steven Barnes, John Hershey, Evan Magill, Kyle Kalbach, Juliana Vinluan, Spencer Hoover
# Creation Date: 2025-02-25, Last edit date: 2025-05-10
# Description: Controller for the UML
from __future__ import annotations

import os
import functools
import logging
from typing import Protocol, Callable
import re

import umlmodel
from umlmodel import UmlProject,Caretaker
from umlclass import UmlClass, UmlField
from umlmethod import UmlMethod, UmlParameter
from umlrelationship import UmlRelationship, RelationshipType
from views.umlview import *
from views.umlview_gui import UmlGuiView
from views.umlview_cli import UmlCliView
from utilities.uml_svg_builder import UmlDiagramSvgBuilder
from utilities.model_utils import UmlModelNamedTupleEncoder
import errors

class UmlCommand(Protocol):
    id:str
    regex:str
    usage:str

class UmlCommands:
    class UmlClass:
        class AddClass(UmlCommand):
            id = r""
            regex = r""
            usage = ""
        
        class RenameClass(UmlCommand):
            id = r""
            regex = r""
            usage = ""
        
        class DeleteClass(UmlCommand):
            id = r""
            regex = r""
            usage = ""
        
        class ListClass(UmlCommand):
            id = r""
            regex = r""
            usage = ""
        
        class ContextClass(UmlCommand):
            id = r""
            regex = r""
            usage = ""

        class HelpClass(UmlCommand):
            id = r""
            regex = r""
            usage = ""

        Commands:list[UmlCommand] = [AddClass, RenameClass, DeleteClass, ListClass, ContextClass, HelpClass]
        Usage:str = HelpClass.usage + "\n".join([c.usage for c in Commands[:-1]])

    class UmlMethodCommands:
        class AddMethod(UmlCommand):
            id = r"method add"
            regex = r"^method add ([A-Za-z][A-Za-z0-9_]*)(\s[A-Za-z][A-Za-z0-9_]*)*$"
            usage = "method add <name> returns <type> params [<param list>]"
        
        class RenameMethod(UmlCommand):
            id = r"method rename"
            regex = r"^method rename (([A-Za-z][A-Za-z0-9_]*)\s){2}arity [0-9]+$"
            usage = "method rename <name> <new name> arity <arity>"
        
        class DeleteMethod(UmlCommand):
            id = r"method delete"
            regex = r"^method delete (([A-Za-z][A-Za-z0-9_]*)\s)arity [0-9]+$"
            usage = "method delete <name> arity <arity>"
        
        class ListMethod(UmlCommand):
            id = r"method list"
            regex = r"^method list$"
            usage = "method list"

        class ContextMethod(UmlCommand):
            id = r"method (?!(add|rename|delete|help|list))"
            regex = r"^method (?!(add|rename|delete|help|list)\s)(([A-Za-z][A-Za-z0-9_]*)\s)arity [0-9]+$"
            usage = "method <name> arity <arity>"
        
        class HelpMethod(UmlCommand):
            id = r"method"
            regex = r"^method (help){0,1}$"
            usage = "method commands:\n"
        
        Commands:list[UmlCommand] = [AddMethod, RenameMethod, DeleteMethod, ListMethod, ContextMethod, HelpMethod]
        Usage:str = HelpMethod.usage + "\n".join([c.usage for c in Commands[:-1]])

    class UmlParameterCommands:
        class AddParameter(UmlCommand):
            id = r"parameter add"
            regex = r"^parameter add ([A-Za-z][A-Za-z0-9_]*)$"
            usage = "parameter add <name>"
        
        class RenameParameter(UmlCommand):
            id = r"parameter rename"
            regex = r"^parameter rename ([A-Za-z][A-Za-z0-9_]*) ([A-Za-z][A-Za-z0-9_]*)$"
            usage = "parameter rename <name> <new name>"
            # usage = "parameter replace <name> <new name> <new type>"
        
        class DeleteParameter(UmlCommand):
            id = r"parameter delete"
            regex = r"^parameter delete ([A-Za-z][A-Za-z0-9_]*)$"
            usage = "parameter delete <name>"

        class ListParameter(UmlCommand):
            id = r"parameter list"
            regex = r"^parameter list$"
            usage = "parameter list"
        
        class ClearParameter(UmlCommand):
            id = r"parameter clear all"
            regex = r"^parameter clear all$"
            usage = "parameter clear all"
        
        class ReplaceParameter(UmlCommand):
            id = r"parameter replace all"
            regex = r"^parameter replace all(\s[A-Za-z][A-Za-z0-9_]*)+$"
            usage = "parameter replace all <param list>"
        
        class HelpParameter(UmlCommand):
            id = r"parameter"
            regex = r"^parameter (help){0,1}$"
            usage = "parameter commands:\n"
        
        Commands:list[UmlCommand] = [AddParameter, RenameParameter, DeleteParameter, ListParameter, ClearParameter, ReplaceParameter, HelpParameter]
        Usage:str = HelpParameter.usage + "\n".join([c.usage for c in Commands[:-1]])

    class UmlHistoryCommands:
        class Undo(UmlCommand):
            id = r"undo"
            regex = r"undo"
            usage = "undo"
        
        class Redo(UmlCommand):
            id = r"redo"
            regex = r"redo"
            usage = "redo"
        
        class HelpHistory(UmlCommand):
            id = r"history"
            regex = r"history"
            usage = "history commands:\n"
        
        Commands:list[UmlCommand] = [Undo, Redo]
        Usage:str = HelpHistory.usage + "\n".join([c.usage for c in Commands[:-1]])

class UmlController:
    HELP_PATH = os.path.join(umlmodel.__DIR__, 'help.txt')
    
    def __init__(self, view:UmlView):
        self.view = view

        self.model:UmlProject = UmlProject()
        self.caretaker:Caretaker = Caretaker(self.model)
        self.active_class:str = None
        self.is_running = False
    
    def _handle_unsaved_changes(func):
        """Decorator to prompt for unsaved changes."""
        @functools.wraps(func)
        def wrapper(self:UmlController, *args, **kwargs):
            #print("[controller::_handle_unsaved_changes]", kwargs, args)
            try:
                override = args[1]
            except:
                override = False
            # override = kwargs.get("override") or False
            if self.model and self.model.has_unsaved_changes and not override:
                if isinstance(self.view, UmlGuiView):
                    raise errors.FileHasUnsavedChangesException()
                # prompt = "A file with that name already exists. Do you want to override it? Y/N.\
                #     \nWARNING: this will erase the old file's contents. "
                # if not self.view.prompt_user(prompt, None):
                #     return
                
                prompt = "The current project has unsaved changes. Would you like to save before continuing?"

                if self.view.prompt_user(prompt, None):
                    self.save_project(self.model._save_path)
                    # if not self.model._save_path:
                    #     #likely need changed for view with mvc
                    #     self.get_filepath_from_user()
                    #     self.model._save_path = self._current_filepath
                    # self.save_project(None)
                    # self.save_project(self.model._save_path)
                # elif user_response.lower() != 'n':
                #     self.inform_invalid_command(user_response)
                #     return wrapper(self, *args, **kwargs)
            
            return func(self, *args, **kwargs)
        return wrapper
    
    def _requires_active_project(func):
        """Decorator to validate a project has been loaded.
        
        Exceptions:
            NoActiveProjectException
        """
        @functools.wraps(func)
        def wrapper(self:UmlController, *args, **kwargs):
            if self.model is None:
                raise errors.NoActiveProjectException()
            return func(self, *args, **kwargs)
        return wrapper
    
    def _requires_active_class(func):
        """Decorator to validate a class context exists.
        
        Exceptions:
            NoActiveClassException
        """
        @functools.wraps(func)
        def wrapper(self:UmlController, *args, **kwargs):
            if self.view.active_class is None:
                raise errors.NoActiveClassException()
            return func(self, *args, **kwargs)
        return wrapper

    def _requires_active_method(func):
        @functools.wraps(func)
        def wrapper(self:UmlController, *args, **kwargs):
            if self.view.active_method is None:
                raise errors.NoActiveMethodException()
            return func(self, *args, **kwargs)
        return wrapper

    def _backup_memento(func):
        @functools.wraps(func)
        def wrapper(self:UmlController, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                self.caretaker.backup()
                return result
            except:
                raise
        return wrapper

    @_backup_memento
    @_handle_unsaved_changes
    def load_project(self, filepath:str, override:bool = False) -> None:
        """Load the project at the provided filepath.

        Params:
            filepath: string
        Returns:
            None
        Exceptions:
            InvalidFileException
        """
        # validate beforehand to keep current project open
        self.model._validate_filepath(filepath)
        # create new project, this may need moved to model
        loaded_model = UmlProject()
        loaded_model.load(filepath)
        self.model = loaded_model
        # save file path to keep from prompting when user saves,
        # since overriding should not be concern if same as loaded file

    @_requires_active_project
    def save_project(self, filename:str, override:bool = False) -> None:
        """
        Saves the currently opened project using the given filepath.\n
        If file already exists, asks the user if they want to override it.\n
        If filename is None, then use existing filename in project
        
        Params:
            filename: name of the file to save to
        Returns:
            None
        Exceptions:
            InvalidFileException if filename was not a json file
        """
        # validate filename is json and set it
        if filename:
            if not self.model.is_json_file(filename):
                raise errors.InvalidFileException()
            
            if self.model._save_path != filename and self.model._filepath_exists(filename) and not override:
                if isinstance(self.view, UmlGuiView):
                    raise errors.FileAlreadyExistsException()
                prompt = "A file with that name already exists. Do you want to override it?\
                    \nWARNING: this will erase the old file's contents. "
                if not self.view.prompt_user(prompt, None):
                    return
                
            self.model._save_path = filename
        #set current filepath to ignore save prompts on later saves of file
        self.model.save()
    
    @_backup_memento
    @_handle_unsaved_changes
    def new_project(self, filepath:str, override:bool = False) -> None:
        """
        Creates a new project using the uml project template,
        and stores a filename.
        
        Params:
            filepath: string to be stored for address to save to
        Returns:
            None
        Exceptions:
            InvalidFileException
        """
        if filepath:
            if not self.model.is_json_file(filepath):
                raise errors.InvalidFileException()

            if self.model._filepath_exists(filepath) and not override:
                if isinstance(self.view, UmlGuiView):
                    raise errors.FileAlreadyExistsException()
                prompt = "A file with that name already exists. Do you want to override it?\
                    \nWARNING: this will erase the old file's contents when saving. "
                if not self.view.prompt_user(prompt, None):
                    return

            
        #declare new project, and call "new" method
        self.model = UmlProject()
        self.model._save_path = filepath
        self.model.new()

    def execute_command(self, args:list):
        #if no arguments then don't try to do anything
        if len(args) == 0:
            return
        error_text = f"Invalid command: {' '.join(args)}.  Use command 'help' for a list of valid commands."
        cmd = args[0].lower()

        if cmd == 'back':
            self.command_back()

        elif cmd == 'class' and len(args) >= 2 and args[1].lower() == 'add':
            if len(args) == 2:
                args.extend(self.view.get_user_input("Enter new class name ").split())
            self.command_add_umlclass(args[2])

        elif cmd == 'delete':
            override = False
            if len(args) == 2:
                override = args[1] == "True"
            self.command_delete_umlclass(override)

        elif cmd == 'rename':
            #ask for rest of input
            if len(args) == 1:
                args.extend(self.view.get_user_input("Enter new class name ").split())
            self.command_rename_umlclass(args[1])

        elif cmd == 'field':
            # TODO - Align this to prompt for additional input.
            if args[1].lower() in ['add','rename'] and len(args) < 4:
                self.view.handle_exceptions(error_text)
            elif len(args) < 3:
                self.view.handle_exceptions(error_text)
            elif args[1].lower() in ['add', 'rename', 'delete']:
                self.command_field(args)
            else:
                self.view.handle_exceptions(error_text)

        #commands that function differently based on whether in or out of a class
        elif cmd == 'class':
            #ask for rest of input
            if len(args) == 1:
                args += self.view.get_user_input("Enter class name ").split()
            self.command_class(args[1])
            
        elif cmd == 'list':
            self.command_list()

        #commands that function either in or out of a class context
        elif cmd == 'relation':
            # TODO - Align this to prompt for additional input.
            if len(args) < 2:
                self.view.handle_exceptions(error_text)
            elif args[1].lower() in ['add', 'set', 'delete', 'list']:
                self.command_relation(args)
            else:
                self.view.handle_exceptions(error_text)

        elif cmd == 'method':
            self.command_method(args)

        elif cmd == 'parameter':
            self.command_parameter(args)

        elif cmd == 'help':
            self.command_show_help()
        
        elif cmd == 'quit':
            self.command_quit()

        elif cmd == 'save':
            # if no filename specified and current save path exists,
            # then call without filepath
            #print("[execute_command(save)]", args)
            if len(args) == 1 and self.model._save_path:
                args.append(None)
            else:
                #if no save filepath but only one arg then request filepath
                if len(args) == 1 and isinstance(self.view, UmlCliView):
                    args.append(self.view.get_user_input("enter file name: "))
            override = False
            if len(args) == 3:
                override = args[2] == "True"
            self.save_project(args[1], override)
            
        elif cmd == 'new':
            # if only new is specified, then assume file will be provided at save
            if len(args) == 1:
                #if input filename is not, then it is not set
                args.append(None)
            override = False
            if len(args) == 3:
                override = args[2] == "True"
            # if filename is provided, then take it, but
            # don't use to create file at this time
            self.new_project(args[1], override)
            
        elif cmd == 'load':
            #ask for rest of input
            override = False
            if len(args) == 1:
                args.append(self.view.get_user_input("Enter project file name: "))
            if len(args) == 3:
                override = args[2] == "True"
            self.load_project(args[1], override)
        
        elif cmd == 'undo':
            self.command_undo()
        
        elif cmd == 'redo':
            self.command_redo()

        elif cmd == 'export':
            self.command_export(args[1])

        else:
            self.view.handle_exceptions(error_text)

    def command_show_help(self):
        """Command: help  
        Displays help menu.
        """
        with open(self.HELP_PATH, "r") as f:
            self.view.handle_exceptions(f.read())

    def command_back(self) -> None:
        """Brings terminal out of class context"""
        if self.view.active_method:
            self.view.set_active_method(None)
        elif self.view.active_class:
            self.view.set_active_class(None)

    @_requires_active_project
    def command_class(self, name:str) -> None:
        """enters the terminal into the class context with the specified class name

        Params:   
            name: the name of the class to enter the context of
        Exceptions:
            NoActiveProjectException
        """
        if self.view.active_class and self.view.active_class == name:
            return
        #store temp to keep from making a new class if user didn't want to
        temp_class = self.model.get_umlclass(name)
        if not temp_class:
            #ask user if they want to create a new class, if it doesn't already exist
            prompt = "that class does not yet exist. Do you want to create it?"
            if self.view.prompt_user(prompt,None):
                self.command_add_umlclass(name)
        else:
            self.view.set_active_class(temp_class.class_name)

    @_backup_memento
    def command_add_umlclass(self, name:str) -> None:
        """adds the specified class name to the project
        
        Exceptions:
            DuplicateClassException
        """
        self.model.add_umlclass(name)
        self.view.set_active_class(name)

    @_backup_memento
    @_requires_active_class
    def command_update_umlclass_position(self, x_pos:float, y_pos:float):
        """moves the UmlClass in the current context to the specified position
        """
        # may want to move this typechecking later
        if type(x_pos) != float or type(y_pos) != float:
            raise errors.InvalidPositionArgsException()
        #use model method
        self.model.update_position_umlclass(self.view.active_class, x_pos, y_pos)
        
    
    @_requires_active_class
    def command_delete_umlclass(self, override:bool = False):
        """Removes the UmlClass in the current context from the project.
        Prompts and informs the user to delete relationships.
        
        Exceptions:
            NoActiveClassException
        """        
        # response is now a bool, equivalent to True=Y,False=N
        # if the user replied N, cancel action
        if not override:
            # Confirm with user
            prompt = "Deleting a class will also remove its relationships. Do you want to continue?"
            # return self.view.prompt_user(prompt, lambda: self.command_delete_umlclass(True))
            if not self.view.prompt_user(prompt, None):
                return

        # Remove from project
        self.model.delete_umlclass(self.view.active_class)
        self.view.set_active_class(None)

    @_backup_memento
    @_requires_active_class
    def command_rename_umlclass(self, name:str):
        """Renames the UmlClass in the current context.
        
        Params:
            name: the new name for the class.
        Exceptions:
            NoActiveClassException
        """
        self.model.rename_umlclass(self.view.active_class, name)
        self.view.set_active_class(name)

    @_requires_active_class
    def command_field(self, args:list[str]):
        """Parses additional args for field commands.
        
        Params:
            args: string list of additional args
        Exceptions:
            NoActiveClassException
        """
        cmd = args[1].lower()
        
        if cmd == 'add':
            self.command_add_field(args[2], args[3])
        elif cmd == 'delete':
            self.command_delete_field(args[2])
        elif cmd == 'rename':
            self.command_rename_field(args[2], args[3])

    @_backup_memento
    @_requires_active_class
    def command_add_field(self, name:str, type:str) -> None:
        """Adds an field to the UmlClass in current context.
        
        Exceptions:
            NoActiveClassException
        """
        #active class is currently a string so get the reference from project
        # self.model.get_umlclass(self.view.active_class).add_field(name)
        self.model.add_field(self.view.active_class, name, type)

    @_backup_memento
    @_requires_active_class
    def command_delete_field(self, name:str) -> None:
        """Deletes an field from the UmlClass in the current context.
        
        Exceptions:
            NoActiveClassException
        """
        # self.model.get_umlclass(self.view.active_class).remove_field(name)
        self.model.delete_field(self.view.active_class, name)

    @_backup_memento
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
        # self.model.get_umlclass(self.view.active_class).rename_field(oldname, newname)
        self.model.rename_field(self.view.active_class, oldname, newname)
    
    @_requires_active_project
    def command_list(self) -> None:
        """
        Displays list of classes when out of class context,
        and displays class contents when in a class

        Exceptions:
            NoActiveProjectException
        """
        if not self.view.active_class:
            data = self._get_model_as_data_object()
            self.view.render_umlproject(data)
        else:
            #find the class to render
            rend_class = self.model.get_umlclass(self.view.active_class)
            data = self._get_class_data_object(rend_class)
            self.view.render_umlclass(data)
    
    @_requires_active_project
    def command_relation(self, args:list[str]):
        """Parses additional args for relation commands.
        
        Params:
            args: string list of additional args
        Exceptions:
            NoActiveProjectException
        """        
        cmd = args[1].lower()
        #since delete doesn't need a relation type do separately
        error_text = "Failed: relation endpoints not specifed\n\
                    proper format: relation <action> srcname destname"
        #check for list and delete here since they need less args
        if cmd == 'list':
            self.command_list_relation()
        elif cmd == 'delete':
            if len(args) < 4 :
                self.view.handle_exceptions(error_text)
                return
            self.command_delete_relation(args[2], args[3])
        #parse for 4th relation arg if not deleting
        elif len(args) < 4:
            self.view.handle_exceptions(error_text + " <type>")
            return
        elif len(args) < 5:
            args.append(self.view.get_user_input("Valid relation types are "\
                + UmlRelationship.valid_relation_types()\
                + "\nEnter type: "))
        if cmd == 'add':
            self.command_add_relation(args[2], args[3], args[4])
        elif cmd == 'set':
            self.command_set_relation(args[2], args[3], args[4])

    @_backup_memento
    @_requires_active_project
    def command_add_relation(self, source:str, destination:str, relationship_type:str) -> None:
        """Adds a relationship.
        
        Params:
            source: a class name owning the source
            destination: a class name owning the destination
            relationship_type: the name of the relationship type
        Exceptions:
            NoActiveProjectException
            NoSuchObjectError
        """
        self.model.add_relationship(source, destination, relationship_type)

    @_backup_memento
    @_requires_active_project
    def command_set_relation(self, source:str, destination:str, relationship_type:str) -> None:
        """Sets the type of an existing relationship.
        
        Params:
            source: a class name owning the source
            destination: a class name owning the destination
            relationship_type: the type of relationship that the relationship should be given
        Exceptions:
            NoActiveProjectException
            NoSuchObjectError
        """
        self.model.set_type_relationship(source, destination, relationship_type)

    @_backup_memento
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
        self.model.delete_relationship(source, destination)

    @_requires_active_project
    def command_list_relation(self):
        """Display all relationships."""
        for relation in self.model.relationships:
            data = self._get_relation_data_object(relation)
            self.view.render_umlrelationship(data)

    @_requires_active_class
    def command_method(self, args:list[str]):
        """"""
        print(args)
        command = " ".join(args)
        umlcommand:UmlCommand = None
        command_match = False
        for c in UmlCommands.UmlMethodCommands.Commands:
            command_match = re.search(c.regex, command) or re.search(c.id, command)
            if command_match:
                umlcommand = c
                break
        
        if umlcommand == UmlCommands.UmlMethodCommands.HelpMethod:
            self.view.handle_exceptions(UmlCommands.UmlMethodCommands.Usage)
            return

        if umlcommand and re.search(umlcommand.regex, command) is None:
            self.view.handle_exceptions(f"Failed: Invalid command.\nUsage: {umlcommand.usage}")
            return
        
        active_class = self.view.active_class

        if umlcommand == UmlCommands.UmlMethodCommands.AddMethod:
            methodname = args[2]
            returntype = args[4]
            methodparams = args[5:]

            paramlist = []
            for i in range(0,len(methodparams),2):
                paramlist.append((methodparams[i],methodparams[i+1]))
            print(methodparams)
            print(paramlist)
            self.model.add_method(active_class, methodname, returntype , paramlist)
        elif umlcommand == UmlCommands.UmlMethodCommands.RenameMethod:
            oldname = args[2]
            newname = args[3]
            overload_id = int(args[5])
            self.model.rename_method(active_class, oldname, newname, overload_id)
            self.set_active_method(newname, overload_id)
        elif umlcommand == UmlCommands.UmlMethodCommands.DeleteMethod:
            methodname = args[2]
            overload_id = int(args[4])
            self.model.delete_method(active_class, methodname, overload_id)
        elif umlcommand == UmlCommands.UmlMethodCommands.ListMethod:
            umlclass = self.model.get_umlclass(active_class)
            data_object = self._get_class_data_object(umlclass)
            for m in data_object.methods:
                self.view.render_umlmethod(m)
        elif umlcommand == UmlCommands.UmlMethodCommands.ContextMethod:
            methodname = args[1]
            overload_id = int(args[3])
            self.set_active_method(methodname, overload_id)
        elif umlcommand == UmlCommands.UmlMethodCommands.HelpMethod:
            self.view.handle_exceptions(UmlCommands.UmlMethodCommands.Usage)

    @_requires_active_class 
    def set_active_method(self, name:str, arity:int):
        self.model.get_umlmethod(self.view.active_class, name, arity)
        self.view.set_active_method((name, arity,))
        
    @_requires_active_project
    def command_undo(self):
        self.caretaker.undo()
    
    @_requires_active_project
    def command_redo(self):
        self.caretaker.redo()

    @_requires_active_method
    def command_parameter(self, args:list[str]):
        command = " ".join(args)
        umlcommand:UmlCommand = None
        command_match = False

        for c in UmlCommands.UmlParameterCommands.Commands:
            command_match = re.search(c.regex, command) or re.search(c.id, command)
            if command_match:
                umlcommand = c
                break
        
        if umlcommand == UmlCommands.UmlParameterCommands.HelpParameter:
            self.view.handle_exceptions(UmlCommands.UmlParameterCommands.Usage)
            return

        if umlcommand and re.search(umlcommand.regex, command) is None:
            self.view.handle_exceptions(f"Failed: Invalid command.\nUsage: {umlcommand.usage}")
            return
        
        active_class = self.view.active_class
        active_method, arity = self.view.active_method

        if umlcommand == UmlCommands.UmlParameterCommands.AddParameter:
            self.model.add_parameter(active_class, active_method, arity, args[2])
            self.set_active_method(active_method, arity + 1)
        elif umlcommand == UmlCommands.UmlParameterCommands.RenameParameter:
            self.model.rename_parameter(active_class, active_method, arity, args[2], args[3])
        elif umlcommand == UmlCommands.UmlParameterCommands.DeleteParameter:
            self.model.delete_parameter(active_class, active_method, arity, args[2])
            self.set_active_method(active_method, arity - 1)
        elif umlcommand == UmlCommands.UmlParameterCommands.ListParameter:
            umlclass = self.model.get_umlclass(active_class)
            data_object = self._get_class_data_object(umlclass)
            for m in data_object.methods:
                if m.name == active_method and len(m.params) == arity:
                    self.view.render_umlmethod(m)
                    break
        elif umlcommand == UmlCommands.UmlParameterCommands.ClearParameter:
            self.model.clear_all_parameters(active_class, active_method, arity)
            self.set_active_method(active_method, 0)
        elif umlcommand == UmlCommands.UmlParameterCommands.ReplaceParameter:
            parameters = args[3:]
            self.model.replace_all_parameters(active_class, active_method, arity, parameters)
            self.set_active_method(active_method, len(parameters))
        elif umlcommand == UmlCommands.UmlParameterCommands.HelpParameter:
            self.view.handle_exceptions(UmlCommands.UmlParameterCommands.Usage)

    def command_export(self, filename:str):
        model = UmlModelNamedTupleEncoder().encode(self.model)
        builder = UmlDiagramSvgBuilder(model)
        builder.produce_svg_part()

        if not filename:
            if self.model._save_path:
                filename = self.model._save_path.replace(".json", ".svg")
            else:
                import datetime as dt
                timestamp = dt.datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"uml_diagram_{timestamp}.svg"
        
        with open(filename, "w") as f:
            f.write(builder.image.xml)

    def _get_model_as_data_object(self) -> UmlProjectData:
        classes = list(map(self._get_class_data_object, self.model.classes.values()))
        relationsips = list(map(self._get_relation_data_object, self.model.relationships))
        return UmlProjectData(classes, relationsips)

    def _get_class_data_object(self, umlclass:UmlClass) -> UmlClassData:
        def get_field_data_object(umlfield:UmlField) -> UmlFieldData:
            return UmlFieldData(umlfield.name, umlfield.type)
        
        def get_method_data_object(umlmethod:UmlMethod) -> UmlMethodData:
            def get_param_data_model(umlparam:UmlParameter) -> UmlMethodParamData:
                return UmlMethodParamData(umlparam.name,umlparam.umltype)
            params = list(map(get_param_data_model, umlmethod.params))
            return UmlMethodData(umlmethod.name,umlmethod.return_type ,params)
        
        fields = list(map(get_field_data_object, umlclass.class_fields.values()))
        methods = []
        for _m in umlclass.class_methods.values():
            for m in _m.values():
                methods.append(get_method_data_object(m))
        #new position values
        x_pos = umlclass.class_pos_x
        y_pos = umlclass.class_pos_y
        
        return UmlClassData(umlclass.class_name, fields, methods, x_pos, y_pos)
    
    def _get_relation_data_object(self, umlrelation:UmlRelationship) -> UmlRelationshipData:
        r = UmlRelationshipData(umlrelation.relationship_type.name.capitalize(), umlrelation.source_class.class_name, umlrelation.destination_class.class_name)
        return r

    def run(self):
        """Runs the application."""
        self.is_running = True

        while self.is_running:
            """"""
            try:
                command = self.view.get_user_command()
                self.execute_command(command)
            # except errors.NoActiveProjectException:
            #     self.view.handle_exceptions("No project has been loaded. Use command: \
            #         load <filepath> or new <filepath> to get started.")
            # except errors.NoActiveClassException:
            #     self.view.handle_exceptions("No active class selection. Use command: class <class name> to select a class.")
            # except errors.DuplicateClassException:
            #     self.view.handle_exceptions("Failed: A class with that name already exists in this project.")
            # except errors.DuplicateFieldException:
            #     self.view.handle_exceptions("Failed: A field with that name already exists on this class.")
            # except errors.InvalidFileException:
            #     self.view.handle_exceptions("Invalid file: Use command: save <filename.json> to save to a file, \
            #         \n command: save to save to current loaded/saved file, \
            #         \n or command: load <filename.json> to load a file that exists \
            #         \n in current folder, or specify subfolder with <filepath/filename.json>")
            # except errors.DuplicateRelationshipException:
            #     self.view.handle_exceptions("Failed: This relationship already exists in this project.")
            # except errors.NoSuchObjectException as nso_e:
            #     self.view.handle_exceptions(f"Failed: That {nso_e.object_type} does not exist.")
            # except errors.InvalidNameException:
            #     self.view.handle_exceptions("Failed: That name contains invalid characters, or begins with a number.")
            # except errors.MethodOverloadNotExistsException:
            #     self.view.handle_exceptions("Failed: The arity level does not exist for this method.")
            # except errors.NoActiveMethodException:
            #     self.view.handle_exceptions("Failed: Not in a method context. Use: method help")
            # except errors.DuplicateMethodOverloadException:
            #     self.view.handle_exceptions("Failed: An arity level already exists for the target method.")
            # except errors.FileAlreadyExistsException:
            #     self.view.handle_exceptions("Warning: A file with that name already exists.  Would you like to override the file?")
            except errors.UMLException as uml_e:
                # self.view.handle_exceptions(f"Operation failed:UML Error:{uml_e}")
                self.view.handle_umlexception(uml_e)
            except EOFError:
                self.is_running = False
            except Exception as e:
                self.view.handle_exceptions(f"Operation failed:UML Error:{e}")
                #raise e
                logging.info(f" unknown error occured: {e.args}")
            finally:
                self._command = None


    @_handle_unsaved_changes
    def command_quit(self):
        """"""
        self.is_running = False
        self.view.quit()

