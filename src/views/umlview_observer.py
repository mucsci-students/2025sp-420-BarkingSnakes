# Filename: umlview_observer.py
# Authors: Steven Barnes, John Hershey, Evan Magill, Kyle Kalbach, Spencer Hoover, Juliana Vinluan
# Date: 2025-04-05
# Description: View (MVC) for UML program using observer and command pattern.


from abc import abstractmethod

from umlcommands.base_commands import UmlCommand, TypedCommand
from umlobserver import UmlSubject, UmlObserver, BaseSubject, CommandSubject
import errors

class UmlViewObserver(BaseSubject, UmlObserver):
    """"""
    def __init__(self):
        BaseSubject.__init__(self)
        self.running = False
    
    def update(self, subject:UmlSubject):
        if isinstance(subject, CommandSubject):
            if isinstance(subject.cmd, TypedCommand) and subject.cmd.__DRIVER_TYPE__ == type(self):
                subject.cmd.set_driver(self)
            subject.cmd.execute()
            subject.detach(self)
    
    @abstractmethod
    def parse_command(self, cmd_string:str) -> UmlCommand:
        """Logic to parse command strings and return an appropriate UmlCommand."""
    
    def handle_command(self, cmd:UmlCommand):
        """Creates a CommandSubject and notifies UmlViewObservers observers a
        command is ready to execute."""
        if cmd:
            command = CommandSubject(cmd)
            if isinstance(cmd, TypedCommand) and cmd.__DRIVER_TYPE__ == type(self):
                command.attach(self)
            else:
                command.attach_many(self._observers)
            command.notify()
    
    @abstractmethod
    def handle_umlexception(self, exception:errors.UMLException):
        """Logic to handle what to do with a UmlException."""

    @abstractmethod
    def start(self):
        """Logic needed to run the UmlViewObserver."""

    @abstractmethod
    def shutdown(self):
        """Logic needed to shutdown and stop the UmlViewObserver from running."""