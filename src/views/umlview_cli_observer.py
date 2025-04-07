import sys
import re

from umlcommands.base_commands import CommandOutcome, CommandResult, CallbackCommand
from views.umlview_observer import UmlViewObserver, UmlCommand, CommandSubject, errors
import umlcommands.controller_commands as c_cmd
from umlclass import UmlClass, UmlMethod
from umlrelationship import RelationshipType, UmlRelationship

class UmlViewCliObserver(UmlViewObserver):
    """"""
    import utilities.cli_utils as cli
    _ec = cli.get_escape_char()
    _getch = cli.getch

    DEFAULT_PROMPT = "BS-uml"
    active_class:UmlClass = None
    active_method:UmlMethod = None

    def get_user_input(self, tcompletes:list[str]) -> str:
        """"""
        user_input = ""
        predict = ""
        s_idx = 0
        offset_left = 0

        sys.stdout.write(self.prompt)
        sys.stdout.flush()
        while True:
            c = self._getch().decode()
            if self._char_is_special(c):
                c = self._getch().decode()
                if c == "K": # left arrow
                    """Move left"""
                    if s_idx > 0:
                        sys.stdout.write(f"{self._ec}[D")
                        offset_left += 1
                    s_idx = max(0, s_idx - 1)
            elif c == "\r": # enter (readline)
                sys.stdout.write("\r" + self.prompt + user_input + "\n")
                sys.stdout.flush()
                return user_input
            elif c == "\t": # tab
                user_input += predict
                sys.stdout.write("\r" + self.prompt + user_input)
                sys.stdout.flush()
                s_idx = len(user_input)
                offset_left = 0
            elif c == "\u0008" or c == "\x7f": # backspace
                if user_input != "":
                    user_input = user_input[:-1]
                    s_idx = len(user_input)
                sys.stdout.write(f"{self._ec}[2K\r" + self.prompt + user_input) # \033 is oct for \u001b
                sys.stdout.flush()
            elif c == "\x03": # ctrl+c
                user_input += "ctrl+c"
            elif c == "\x04": # ctrl+d
                user_input = "quit"
                return user_input
            else:
                user_input = user_input[:s_idx] + c + user_input[s_idx:]
                # s += c
                s_idx += 1
                sys.stdout.write("\r" + self.prompt + user_input)
                if offset_left > 0:
                    sys.stdout.write(f"{self._ec}[{offset_left}D")
                sys.stdout.flush()
        
            if user_input != "":
                    for tcomplete in tcompletes:
                        if tcomplete.startswith(user_input):
                            predict = tcomplete[len(user_input):]
                            sys.stdout.write(f"{self._ec}[K{self._ec}[90m" + predict + f"{self._ec}[0m" + "\u0008" * len(predict))
                            break
                        sys.stdout.write(f"{self._ec}[K")

    def _char_is_special(self, char:str) -> bool:
        """Checks if the first keypress was a special character."""
        return char == '\000' or char == '\xe0'

    def parse_command(self, cmd_string:str) -> UmlCommand:
        """Logic to parse command strings and return an appropriate UmlCommand."""
        # if cmd_string == "quit":
        #     cmd = self.COMMANDS.ExitCommand()
        #     cmd.set_driver(self)
        #     return cmd
        # else:
        cmd_args = tuple(cmd_string.split(" "))
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
        prompt = f"{self._ec}[1;31m{self.DEFAULT_PROMPT}{self._ec}[0m"
        if self.active_class:
            classname = self.active_class.class_name
            prompt += f"{self._ec}[36m[{classname}]{self._ec}[0m"
        if self.active_method:
            methodname = self.active_method.name
            paramlist = ",".join(self.active_method.overloadID.split(" "))
            rtype = self.active_method.return_type
            prompt += f"{self._ec}[33m[+{methodname}({paramlist}) -> {rtype}]{self._ec}[0m"
        return rf"{prompt}{self._ec}[1;31m>{self._ec}[0m "

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
                raise result.exception
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
        while self.running:
            try:
                tcompletes = self._calculate_tab_completion_list()
                cmd_string = self.get_user_input(tcompletes)
                if cmd_string:
                    _command = self.parse_command(cmd_string)
                    self.handle_command(_command)
                    self.handle_command_result(_command)
            except Exception as e:
                # print(f"ERROR: Something went wrong. ({e})")
                raise e

    def shutdown(self):
        """Logic needed to shutdown and stop the UmlViewObserver from running."""
        self.running = False

