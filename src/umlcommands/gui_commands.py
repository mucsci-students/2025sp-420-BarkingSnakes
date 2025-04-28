from flask import Response

from umlcommands.base_commands import UmlCommand, CallbackCommand, CommandOutcome, TypedCommand, PromptCommand, BinaryPromptCommand, InputPromptCommand, PromptRequester
from views.umlview_gui_observer import UmlViewGuiObserver

class GuiCommand(TypedCommand[UmlViewGuiObserver]):
    """A command specific for the UmlGuiView."""
    
    __DRIVER_TYPE__ = UmlViewGuiObserver

class HttpResponseCommand(GuiCommand):
    """"""

    @property
    def http_response(self) -> Response:
        return self._response

class GuiBinaryPromptCommand(BinaryPromptCommand[GuiCommand]):
    def execute(self):
        self._outcome = None
        self.set_result(CommandOutcome.SUCCESS)
    
class GuiInputPromptCommand(InputPromptCommand[GuiCommand]):
    def execute(self):
        self._output = None
        self.set_result(CommandOutcome.SUCCESS)

class GuiPromptRequester(PromptRequester):

    def get_prompt(self, prompt_type:PromptCommand, message:str) -> PromptCommand:
        if issubclass(prompt_type, BinaryPromptCommand):
            return GuiBinaryPromptCommand(message=message)
        
        if issubclass(prompt_type, InputPromptCommand):
            return GuiInputPromptCommand(message=message)