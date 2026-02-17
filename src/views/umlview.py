# Filename: umlview.py
# Authors: Steven Barnes, John Hershey, Evan Magill, Kyle Kalbach, Spencer Hoover, Juliana Vinluan
# Creation Date: 2025-03-01, Last edit Date 2025-5-10
# Description: View (MVC) for UML program.

from dataclasses import dataclass
from typing import Protocol, NamedTuple, Callable
import errors


class UmlFieldData(NamedTuple):
    name:str
    type:str

class UmlMethodParamData(NamedTuple):
    name:str
    type:str

class UmlMethodData(NamedTuple):
    name:str
    return_type:str
    params:list[UmlMethodParamData]
        

class UmlClassData(NamedTuple):
    name:str
    fields:list[UmlFieldData]
    methods:list[UmlMethodData]
    x_pos:float
    y_pos:float

class UmlRelationshipData(NamedTuple):
    relation_type:str
    source:str
    destination:str

class UmlProjectData(NamedTuple):
    classes:list[UmlClassData]
    relationships:list[UmlRelationshipData]


@dataclass
class UmlView(Protocol):

    def prompt_user(self, prompt:str, callback:Callable) -> bool:
        """Shown directly to the user for additional information."""

    def get_user_input(self, text:str) -> str:
        """Shown directly to the user for additional information."""

    def get_user_command(self) -> list:
        """Runs view loop, waiting for user input or action."""

    def handle_exceptions(self, error_text:str):
        """"""

    @property
    def get_umlexception(self) -> errors.UMLException:
        """"""

    def set_callback(self, callback:Callable):
        """"""
    @property
    def callback(self) -> Callable:
        """"""

    @property
    def prompt_response(self) -> bool:
        """"""

    def set_umlexception(self, e:errors.UMLException):
        """"""

    def render_umlproject(self, project:UmlProjectData):
        """"""
    
    def render_umlclass(self, umlclass:UmlClassData):
        """"""

    def render_umlfield(self, umlfield:UmlFieldData):
        """"""

    def render_umlmethod(self, umlmethod:UmlMethodData):
        """"""

    def render_umlmethodparam(self, umlmethodparam:UmlMethodParamData):
        """"""

    def render_umlrelationship(self, umlrelationship:UmlRelationshipData):
        """"""

    def quit(self):
        """"""

    def init(self):
        """"""
    
    ##functions that match between CLI and GUI
    def handle_umlexception(self, uml_exception:errors.UMLException):
        """"""

    def set_active_class(self, name:str):
        """sets the active class\n\nthe same for the gui and cli"""
        self._active_class = name
    
    def set_active_method(self, method:tuple[str, str]):
        """set the active method"""
        self._active_method = method
        
    @property
    def active_class(self) -> str:
        """return the current active class"""
        return self._active_class

    @property
    def active_method(self) -> tuple[str, str]:
        """return active method as a tuple of name and overloadID"""
        return self._active_method