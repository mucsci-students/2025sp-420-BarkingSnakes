import os
from typing import Literal
from umlcommands.base_commands import UmlCommand, CallbackCommand, TypedCommand, PromptCommand, BinaryPromptCommand, InputPromptCommand, PromptRequester, CommandOutcome
from views.umlview_cli_observer import UmlViewCliObserver

from umlclass import UmlClass, UmlMethod
from umlrelationship import RelationshipType, UmlRelationship

__HELP_PATH__  = os.path.join("src", "help.txt")

class CliCommand(TypedCommand[UmlViewCliObserver]):
    """A command specific for the UmlCliView.  The UmlCliView can either be
    passed to the constructor or supplied with the set_cli() method."""

    __DRIVER_TYPE__ = UmlViewCliObserver

class InvalidCommand(CliCommand):
    def execute(self):
        """"""
        print("Invalid command: ", self._args[0])
        self.set_result(CommandOutcome.SUCCESS)

class SetActiveClassCommand(CliCommand):
    def execute(self):
        """"""
        self.driver.active_class = self.umlclass
        self.set_result(CommandOutcome.SUCCESS)
    
    @property
    def umlclass(self) -> UmlClass:
        """"""
        prop_index = 0
        return self._args[prop_index]

class SetActiveMethodCommand(CliCommand):
    def execute(self):
        self.driver.active_method = self.umlmethod
        self.set_result(CommandOutcome.SUCCESS)

    @property
    def umlmethod(self) -> UmlMethod:
        prop_index = 0
        return self._args[prop_index]

class DisplayClassListCommand(CliCommand):
    def execute(self):
        """"""
        if not any(self.umlclasses):
            print("No classes to display.")
        else:
            ec = self.driver._ec
            tcolor = f"{ec}[35m"
            color_clear = f"{ec}[0m"
            for c in self.umlclasses:
                class_string = f"{c.class_name}"
                for f in c.class_fields.values():
                    class_string += f"\n  -{f.name}:{tcolor}{f.type}{color_clear}"
                for _m in c.class_methods.values():
                    for m in _m.values():
                        param_strings = [f"{p.name}:{tcolor}{p.umltype}{color_clear}" for p in m.params]
                        method_string = f"  +{m.name} ({', '.join(param_strings)}) -> {m.return_type}"
                        class_string += f"\n{method_string}"
                print(class_string)
            
        
        self.set_result(CommandOutcome.SUCCESS)

    @property
    def umlclasses(self) -> list[UmlClass]:
        return self._args[0]

class DisplayRelationListCommand(CliCommand):
    def execute(self):
        """"""
        if not any(self.relationships):
            print("No relationships to display.")
        else:
            print("Source\t\tDestination\t\tType")
            for r in self.relationships:
                print(f"{r.source_class.class_name}\t\t{r.destination_class.class_name}\t\t\t{r.relationship_type.name.lower()}")
        self.set_result(CommandOutcome.SUCCESS)
    
    @property
    def relationships(self) -> set[UmlRelationship]:
        return self._args[0]

class RelationTypesCommand(CliCommand):
    def execute(self):
        print(f"Valid Relation Types")
        print(f"  {RelationshipType.AGGREGATION.name.lower()}")
        print(f"  {RelationshipType.COMPOSITION.name.lower()}")
        print(f"  {RelationshipType.INHERITANCE.name.lower()}")
        print(f"  {RelationshipType.REALIZATION.name.lower()}")
        self.set_result(CommandOutcome.SUCCESS)

class BackCommand(CliCommand):
    def execute(self):
        if self.driver.active_method:
            self.driver.active_method = None
        elif self.driver.active_class:
            self.driver.active_class = None
        
        self.set_result(CommandOutcome.SUCCESS)

class ExitCommand(CliCommand):
    def execute(self):
        self.driver.shutdown()
        self.set_result(CommandOutcome.SUCCESS)

class HelpCommand(CliCommand):
    def execute(self):
        """"""
        if os.path.exists(__HELP_PATH__):
            with open(__HELP_PATH__, "r") as f:
                print(f.read())
        
        self.set_result(CommandOutcome.SUCCESS)

class CliBinaryPromptCommand(BinaryPromptCommand[CliCommand]):
    def execute(self):
        user_input = ""
        while not user_input in ["y", "n"]:
            user_input = input(f"{self.message} Y/N: ").lower()
        self._outcome = user_input == "y"
        self.set_result(CommandOutcome.CONTINUE)

class CliInputPromptCommand(InputPromptCommand[CliCommand]):
    def execute(self):
        self._output = ""
        while self._output == "":
            self._output = input(f"{self.message} ")
        self.set_result(CommandOutcome.CONTINUE)


class CliPromptRequester(PromptRequester):

    def get_prompt(self, prompt_type:PromptCommand, message:str) -> PromptCommand:
        if issubclass(prompt_type, BinaryPromptCommand):
            return CliBinaryPromptCommand(message=message)
        
        if issubclass(prompt_type, InputPromptCommand):
            return CliInputPromptCommand(message=message)

CLICOMMANDS = {
    r"^back$": BackCommand,
    r"^relation types$": RelationTypesCommand,
    r"^help$": HelpCommand
}