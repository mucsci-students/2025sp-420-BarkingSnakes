from __future__ import annotations
from abc import ABC, abstractmethod

from umlcontroller import UmlController
from views.umlview_cli_v2 import UmlCliViewV2 as UmlCli

class UmlCommand(ABC):
    """UmlCommand interface."""
    @abstractmethod
    def execute(self):
        """Executes the desired behavior of a command."""

class Callback:
    def callback(self):
        """"""
        self._callback.execute()

    def set_callback(self, callback:UmlCommand):
        self._callback = callback

class BaseCommand(UmlCommand):
    def __init__(self, *args):
        self._args = args

class ControllerCommand(BaseCommand):
    def __init__(self, *args, controller:UmlController = None):
        super().__init__(*args)
        self.controller = controller
    
    def set_controller(self, controller:UmlController):
        self.controller = controller

class CliCommand(UmlCommand):
    def __init__(self, cli:UmlCli = None):
        self.cli = cli

    def set_cli(self, cli:UmlCli):
        self.cli = cli

class StrategicCommand(UmlCommand):
    def execute(self):
        if self.strategy:
            self.strategy.execute()

    def with_strategy(self, strategy) -> UmlCommand:
        self.strategy = strategy