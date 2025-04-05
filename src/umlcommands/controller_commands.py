from base_commands import UmlCommand, ControllerCommand, CallbackCommand

class AddClassCommand(ControllerCommand):
    def execute(self):
        self.controller.add_umlclass(self.name)

    @property
    def name(self) -> str:
        return self._args[-1]
    
class RenameClassCommand(ControllerCommand):
    def execute(self):
        self.controller.command_class(self.oldname)
        self.controller.command_rename_umlclass(self.newname)
    
    @property
    def newname(self) -> str:
        return self._args[-1]
    
    @property
    def oldname(self) -> str:
        # TODO - This probably isn't correct.
        return self._args[-2]

class QuitCommand(ControllerCommand, CallbackCommand):
    def execute(self):
        if self.controller.model.has_unsaved_changes:
            # TODO - Handle prompting for unsaved changes.
            True

UMLCOMMANDS:dict[str, UmlCommand] = {
    r"^class add ([A-Za-z][A-Za-z0-9_]*)$": AddClassCommand,
    r"^class rename ([A-Za-z][A-Za-z0-9_]*)$": RenameClassCommand,
    r"^quit$": QuitCommand
}