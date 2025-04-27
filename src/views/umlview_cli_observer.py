# Filename: umlview_cli_observer.py
# Authors: Steven Barnes, John Hershey, Evan Magill, Kyle Kalbach, Juliana Vinluan, Spencer Hoover
# Date: 2025-02-25, Last edit date: 2025-04-26
# Description: cli observer implementation
from __future__ import annotations
import sys
import re
import cmd
import os

from umlcommands.base_commands import CommandOutcome, CommandResult, CallbackCommand
from views.umlview_observer import UmlViewObserver, UmlCommand, CommandSubject, errors
import umlcommands.controller_commands as c_cmd
from umlclass import UmlClass, UmlMethod
from umlrelationship import RelationshipType, UmlRelationship

class UmlShell(cmd.Cmd):
    """Cmd descendent for handling tab completion and prompting"""
    def set_view(self, view:UmlViewCliObserver):
        self.view = view
        self.prompt = view.prompt

    def completedefault(self, text, line, begidx, endidx):
        offset = len(line) - len(text)
        tcompletes = self.view._calculate_tab_completion_list()
        return [s[offset:] for s in tcompletes if s.startswith(line)]

    def default(self, line):
        try:
            _command = self.view.parse_command(line)
            self.view.handle_command(_command)
            self.view.handle_command_result(_command)
        except Exception as e:
            print(f"ERROR: Something went wrong. ({e})")
        self.prompt = self.view.prompt
        return not self.view.running

    #def do_help(self, arg):
    #    return self.default('help ' + arg)

    # The following functions are needed for tab completion of the first token.
    def do_class(self, arg):
        return self.default('class ' + arg)

    def do_relation(self, arg):
        return self.default('relation ' + arg)

    def do_load(self, arg):
        return self.default('load ' + arg)

    def do_new(self, arg):
        return self.default('new ' + arg)

    def do_save(self, arg):
        return self.default('save ' + arg)

    def do_quit(self, arg):
        return self.default('quit ' + arg)

    def do_list(self, arg):
        return self.default('list ' + arg)

    def do_undo(self, arg):
        return self.default('undo ' + arg)
    
    def do_redo(self, arg):
        return self.default('redo ' + arg)

    def do_EOF(self, arg):
        quit()
    
    def do_terminalclear(self, arg):
        os.system('clear')

    # Though these should only be accessible in certain contexts, to have the words
    # tab complete, we need these here, but that means they will also be options
    # in the other contexts.
    def do_parameter(self, arg):
        return self.default('parameter ' + arg)

    def do_field(self, arg):
        return self.default('field ' + arg)

    def do_method(self, arg):
        return self.default('method ' + arg)
    
    def do_back(self, arg):
        return self.default('back ' + arg)
    
    #maybe put help stuff here possibly dont know lol 
    def help_help(self):
        print("\nhelp\n\
        Display help menu\n\
        \nYou can also use the command \"help <command>\" to get help on a specific command.\n")

    def help_class(self):
        print("\nclass <classname>\n\
        Enters the context for the class with the specified <classname> or prompts you\n\
        to add if it is not an existing class\n\n\
class add <classname>\n\
        Adds the class and enters the context for the class. If a name is not provided,\n\
        it prompts for a name\n\n\
class delete\n\
        Removes the class from the project and all of its relationships.\n\
        Issues a Y/N prompt to confirm the action.\n\n\
rename <new name>\n\
        Renames the class to the provided <new name> or if one was not provided,\n\
        prompts for a new name\n\n\
list\n\
        Displays the current class and its fields, methods and parameters\n\
        in a box.\n\n\
list\n\
        In the project context, displays all classes and their fields, methods and parameter.\n")

    def help_relation(self):
        print("\nrelation add <source class> <destination class> <relationship type>\n\
        Adds a relationship of type <relationship type> from <source class>\n\
        to <destination class>\n\n\
<relation type> is one of:\n\
        \"aggregation\", \"composition\", \"inheritance\", or \"realization\"\n\n\
relation delete <source class> <destination class>\n\
        Deletes a relationship of from <source class> to <destination class>\n\
        if it exists\n\n\
relation set <source class> <destination class> <relationship type>\n\
        Finds the relationship with the specified source and destination, and sets its type.\n\n\
relation list\n\
        Lists all relations in the current project.\n")

    def help_field(self):
        print("\nfield add <field name> <field type>\n\
        Adds the field with name <field name> and <field type> to the class.\n\n\
field delete <field name>\n\
        Deletes the field with name <field name> from the class.\n\n\
field rename <old field name> <new field name>\n\
        Renames the field on the class with <old field name>\n\
        to <new field name>\n")
    
    def help_method(self):
        print("\nmethod add <method name> <method return type> <param1 name>:<param1 type> <param2 name>:<param2 type>...\n\
        Adds the method with name <method name> to the class.\n\n\
method rename <old method name> <new method name> arity <arity>\n\
        Renames the method on the class with <old method name>\n\
        to <new method name>, arity must be specified\n\n\
method delete <method name> <parameter1 type> <parameter2 type> <parameter2 type>...\n\
        Deletes the method with name <method name> from the class.\n\n\
method <method name> <parameter1 type> <parameter2 type> <parameter2 type>...\n\
        Enters the context for the specified method\n")

    def help_parameter(self):
        print("\nparameter add <parameter name>:<parameter type>\n\
        Adds the parameter with name <parameter name> to the class.\n\n\
parameter rename <old parameter name> <new parameter name>\n\
        Renames the parameter on the class with <old parameter name>\n\n\
parameter delete <parameter name>\n\
        Deletes the parameter with name <parameter name> from the class.\n")

    def help_back(self):
        print("\nback\n\
        Exits the current context and returns to the previous one\n")

    def help_undo(self):
        print("\nundo\n\
        Undoes the last command\n")

    def help_redo(self):
        print("\nredo\n\
        Redoes the last command\n")
    #TODO: add this to help.txt

    def help_delete(self):
        print("\ndelete\n\
        Removes the class from the project and all of its relationships.\n\
        Issues a Y/N prompt to confirm the action.\n")

    def help_rename(self):
        print("\nrename <new name>\n\
        Renames the class to the provided <new name> or if one was not provided,\n\
        prompts for a new name\n")

    def help_list(self):
        print("\nlist\n\
        Displays the current class and its fields, methods and parameters\n\
        in a box.\n\n\
list\n\
        In the project context, displays all classes and their fields, methods and parameter.\n") 
        
    def help_load(self):
        print("\nload <filename>\n\
        Load the file at <filename>\n\
        If a project file is open, will prompt to save.\n")
        
    def help_new(self):
        print("\nnew <filename>\n\
        Create a new project file at <filename>\n\
        If a project file is open, will prompt to save.\n")

    def help_save(self):
        print("\nsave\n\
        Save the current file\n")

    def help_quit(self):
        print("\nquit or Ctrl+D\n\
        Quits the program. Prompts to save any unsaved changes.\n")
    
    


class UmlViewCliObserver(UmlViewObserver):
    """View observer for CLI"""
    import utilities.cli_utils as cli
    _ec = cli.get_escape_char()

    DEFAULT_PROMPT = "BS-uml"
    active_class:UmlClass = None
    active_method:UmlMethod = None


    def parse_command(self, cmd_string:str) -> UmlCommand:
        """Logic to parse command strings and return an appropriate UmlCommand."""
        cmd_string = cmd_string.strip()
        cmd_args = tuple(cmd_string.split())# Changed from .split(" "), revert if needed.
        for regex, cmd in c_cmd.UMLCOMMANDS.items():
            if re.search(regex, cmd_string):
                _cmd = cmd(*cmd_args)
                if isinstance(_cmd, c_cmd.QuitCommand):
                    exit_cmd = self.COMMANDS.ExitCommand()
                    exit_cmd.set_driver(self)
                    _cmd.set_callback(exit_cmd)
                if isinstance(_cmd, c_cmd.PromptingCommand):
                    _cmd.set_prompt_requester(self._prompt_requester)
                return _cmd
        
        for regex, cmd in self.COMMANDS.CLICOMMANDS.items():
            if re.search(regex, cmd_string):
                _cmd = cmd(*cmd_args)
                if isinstance(_cmd, self.COMMANDS.CliCommand):
                    _cmd.set_driver(self)
                return _cmd

        return self.COMMANDS.InvalidCommand(cmd_string)

    def _add_callback(self, cmd:CallbackCommand):
        """Logic to handle adding a callback to a command."""


    def handle_umlexception(self, exception:errors.UMLException):
        """Logic to handle what to do with a UmlException."""
        print(exception)

    @property
    def prompt(self) -> str:
        """The CLI prompt to display each loop."""
        prompt = f"{self.DEFAULT_PROMPT}"
        if self.active_class:
            classname = self.active_class.class_name
            prompt += f"[{classname}]"
        if self.active_method:
            methodname = self.active_method.name
            paramlist = ",".join(self.active_method.overloadID.split(" "))
            rtype = self.active_method.return_type
            prompt += f"[+{methodname}({paramlist}) -> {rtype}]"
        return rf"{prompt}> "

    def _calculate_tab_completion_list(self) -> list[str]:
        """Calculates the available options for tab completion."""

        # Base options, always available
        t_base = ["quit", "list", "relation list", "relation types", "undo", "redo"]

        classes:list[UmlClass] = None
        cmd:c_cmd.ListClassesCommand = self.parse_command("class list")
        self.handle_command(cmd)
        result = cmd.get_result()
        if result.outcome == CommandOutcome.SUCCESS:
            classes = cmd.umlclasses
        
        relationships:set[UmlRelationship] = None
        cmd2:c_cmd.ListRelationCommand = self.parse_command("relation list")
        self.handle_command(cmd2)
        result2 = cmd.get_result()
        if result.outcome == CommandOutcome.SUCCESS:
            relationships = cmd2.relationships
            relation_strings = [f"{r.source_class.class_name} {r.destination_class.class_name}" for r in relationships]

        for c1 in classes:
            for c2 in classes:
                relation_string = f"{c2.class_name} {c2.class_name}"
                if relation_string in relation_strings:
                    t_base.append(f"relation delete {relation_string}")
                    t_base.append(f"relation set {relation_string} {RelationshipType.AGGREGATION.name.lower()}")
                    t_base.append(f"relation set {relation_string} {RelationshipType.COMPOSITION.name.lower()}")
                    t_base.append(f"relation set {relation_string} {RelationshipType.INHERITANCE.name.lower()}")
                    t_base.append(f"relation set {relation_string} {RelationshipType.REALIZATION.name.lower()}")
                else:
                    t_base.append(f"relation add {c1.class_name} {c2.class_name} {RelationshipType.AGGREGATION.name.lower()}")
                    t_base.append(f"relation add {c1.class_name} {c2.class_name} {RelationshipType.COMPOSITION.name.lower()}")
                    t_base.append(f"relation add {c1.class_name} {c2.class_name} {RelationshipType.INHERITANCE.name.lower()}")
                    t_base.append(f"relation add {c1.class_name} {c2.class_name} {RelationshipType.REALIZATION.name.lower()}")

        # options available when not in a class context
        if not self.active_class:
            class_base = ["class add "]

            # Add the classes from the model as tab complete options
            if classes:
                for c in classes:
                    class_base.append("class {}".format(c.class_name))
            t_base.extend(class_base)
        else:
            # Options available in a class context
            class_context_base = [
                "back", 
                "field add ", 
                "delete", 
                "rename ",
                "field add ",
                "method add "
            ]

            # Add the class field and method names as tab complete options
            for f in self.active_class.class_fields.keys():
                class_context_base.append(f"field delete {f}")
                class_context_base.append(f"field rename {f} ")
            
            # for _m in cmd.umlclass.class_methods.values():
            for _m in self.active_class.class_methods.values():
                for m in _m.values():
                    method_string = f"{m.name} {m.overloadID}".strip()
                    class_context_base.append(f"method {method_string}")
                    class_context_base.append(f"method delete {method_string}")
            t_base.extend(class_context_base)
            
            if self.active_method:
                method_context_base = [
                    "method rename ", 
                    "parameter add ", 
                    "parameter replace all",
                    "parameter clear all"
                ]

                for p in self.active_method.params:
                    method_context_base.append(f"parameter rename {p.name} ")
                    method_context_base.append(f"parameter delete {p.name}")
                    # method_context_base.append(f"parameter replace {p.name} ")
                
                t_base.extend(method_context_base)
                
        return t_base
            
    def handle_command_result(self, cmd:UmlCommand):
        """Handles additional logic based on the outcomes of a command execution."""
        result = cmd.get_result()

        if result.outcome == CommandOutcome.FAILED:
            if result.ErrorText:
                print("Failed: ", result.ErrorText)
            else:
                print(f"Failed: Something unexpected happened. ({result.exception}:{cmd})")
            return

        if result.outcome == CommandOutcome.EXCEPTION:
            # print(f"ERROR: Something unexpected happened. ({result.exception}:{cmd})")
            # return
            raise result.exception

        if result.outcome == CommandOutcome.SUCCESS:
            """"""
            command:UmlCommand = None
            if isinstance(cmd, (c_cmd.RenameClassCommand, c_cmd.GetUmlClassCommand)):
                command = self.COMMANDS.SetActiveClassCommand(cmd.umlclass)
            if isinstance(cmd, (c_cmd.MethodContextCommand, c_cmd.MethodDeleteCommand, c_cmd.MethodRenameCommand)):
                command = self.COMMANDS.SetActiveMethodCommand(cmd.umlmethod)
            elif isinstance(cmd, c_cmd.ListClassesCommand):
                command = self.COMMANDS.DisplayClassListCommand(cmd.umlclasses)
            elif isinstance(cmd, c_cmd.ListRelationCommand):
                command = self.COMMANDS.DisplayRelationListCommand(cmd.relationships)
            elif isinstance(cmd, self.COMMANDS.BackCommand):
                command = self.parse_command("controller back")
                self.handle_command(command)
                return

            if command:
                self.notify_self(command)

    def notify_self(self, cmd:UmlCommand):
        cmdsub = CommandSubject(cmd)
        cmdsub.attach(self)
        cmdsub.notify()

    def start(self):
        """Logic needed to run the UmlViewObserver."""
        import umlcommands.cli_commands
        self.COMMANDS = umlcommands.cli_commands
        self._prompt_requester = self.COMMANDS.CliPromptRequester()

        self.running = True
        
        shell = UmlShell()
        shell.set_view(self)
        shell.cmdloop()

    def shutdown(self):
        """Logic needed to shutdown and stop the UmlViewObserver from running."""
        self.running = False

