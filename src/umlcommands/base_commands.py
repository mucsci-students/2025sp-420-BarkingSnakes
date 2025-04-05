from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import NamedTuple

from errors import UMLException
from umlcontroller import UmlController
from views.umlview_cli import UmlCliView as UmlCli
from views.umlview_gui import UmlGuiView as UmlGui


class CommandOutcome(Enum):
    FAILED = -1
    SUCCESS = 0
    EXCEPTION = 1
    DEFERRED = 2
    CONTINUE = 3

class UmlCommand(ABC):
    """UmlCommand interface."""
    @abstractmethod
    def execute(self):
        """Executes the desired behavior of a command."""
    
    @abstractmethod
    def get_result(self) -> CommandResult:
        """Retreive the results of the executed command."""
    
    @abstractmethod
    def set_result(self, outcome:CommandOutcome, exception:UMLException = None):
        """Set the results of the executed command.  Typically this would be
        the last line on the execute() method."""

class CommandResult(NamedTuple):
    """A result object used to pass information between a UmlCommand and the
    object which triggered it."""
    command:UmlCommand
    outcome:CommandOutcome
    exception: UMLException

class CallbackCommand:
    """Defines a command which can take a callback command."""
    def callback(self):
        """Executes the callback command."""
        self._callback.execute()

    def set_callback(self, callback:UmlCommand):
        """Sets the callback command."""
        self._callback = callback

class BaseCommand(UmlCommand):
    """The base command with implementations of the UmlCommand interface."""
    def __init__(self, *args, **kwargs):
        self._args = args
        self.kwargs = kwargs
        self._result:CommandResult = None
    
    def get_result(self) -> CommandResult:
        """"""
        return self._result
    
    def set_result(self, outcome:CommandOutcome, exception:UMLException = None):
        """"""
        result = CommandResult(self, outcome, exception)
        self._result = result

class ControllerCommand(BaseCommand):
    """A command specific for the UmlController.  The controller can either be
    passed to the constructor or supplied with the set_controller() method."""
    def __init__(self, *args, controller:UmlController = None):
        super().__init__(*args)
        self.controller = controller
    
    def set_controller(self, controller:UmlController):
        self.controller = controller

class CliCommand(UmlCommand):
    """A command specific for the UmlCliView.  The UmlCliView can either be
    passed to the constructor or supplied with the set_cli() method."""
    def __init__(self, cli:UmlCli = None):
        self.cli = cli

    def set_cli(self, cli:UmlCli):
        self.cli = cli

class GuiCommand(UmlCommand):
    """A command specific for the UmlGuiView.  The UmlGuiView can either be
    passed to the constructor or supplied with the set_gui() method."""
    def __init__(self, gui:UmlGui = None):
        self.gui = gui

    def set_gui(self, gui:UmlGui):
        self.gui = gui

class StrategicCommand(UmlCommand):
    def execute(self):
        if self.strategy:
            self.strategy.execute()

    def with_strategy(self, strategy) -> UmlCommand:
        self.strategy = strategy