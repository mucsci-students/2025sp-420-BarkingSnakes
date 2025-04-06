from umlcommands.base_commands import UmlCommand, CallbackCommand, TypedCommand
from views.umlview_cli_observer import UmlViewCliObserver


class CliCommand(TypedCommand[UmlViewCliObserver]):
    """A command specific for the UmlCliView.  The UmlCliView can either be
    passed to the constructor or supplied with the set_cli() method."""

    __DRIVER_TYPE__ = UmlViewCliObserver

class EchoCommand(CliCommand):
    def execute(self):
        """"""
        print(self._args, self._kwargs)

class ExitCommand(CliCommand):
    def execute(self):
        self.driver.shutdown()