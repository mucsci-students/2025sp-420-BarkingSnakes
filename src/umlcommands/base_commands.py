from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import NamedTuple, TypeVar, Generic

from errors import UMLException

T = TypeVar("T")

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
        self._kwargs = kwargs
        self._result:CommandResult = None
    
    def get_result(self) -> CommandResult:
        """"""
        return self._result
    
    def set_result(self, outcome:CommandOutcome, exception:UMLException = None):
        """"""
        result = CommandResult(self, outcome, exception)
        self._result = result

class TypedCommand(BaseCommand, Generic[T]):
    __DRIVER_TYPE = None
    def __init__(self, driver:T = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._driver = driver

    def set_driver(self, driver:T):
        self._driver = driver
    
    def get_driver(self) -> T:
        return self._driver

    @property
    def driver(self) -> T:
        return self.get_driver()

class StrategicCommand(UmlCommand):
    def execute(self):
        if self.strategy:
            self.strategy.execute()

    def with_strategy(self, strategy) -> UmlCommand:
        self.strategy = strategy