from umlcommands.base_commands import UmlCommand, TypedCommand
from umlobserver import UmlSubject, UmlObserver, BaseSubject, CommandSubject
from umlmodel import UmlProject, UmlClass, UmlMethod
import errors

class UmlControllerObserver(BaseSubject, UmlObserver):

    def __init__(self):
        BaseSubject.__init__(self)
        self.running = False
        self.model:UmlProject = UmlProject()
        self.active_class:UmlClass = None
        self.active_method:UmlMethod = None

    def update(self, subject:UmlSubject):
        """"""
        if isinstance(subject, CommandSubject):
            if isinstance(subject.cmd, TypedCommand) and subject.cmd.__DRIVER_TYPE__ == type(self):
                subject.cmd.set_driver(self)
            subject.cmd.execute()
            subject.detach(self)
    
    def run(self):
        import time

        self.running = True
        while self.running:
            time.sleep(0.1)
    
    def stop(self):
        self.running = False