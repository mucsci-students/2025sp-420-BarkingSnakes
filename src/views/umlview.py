# Filename: umlview.py
# Authors: Steven Barnes, John Hershey, Evan Magill, Kyle Kalbach, Spencer Hoover, Juliana Vinluan
# Date: 2025-03-01
# Description: View (MVC) for UML program.

from dataclasses import dataclass
from typing import Protocol, NamedTuple


class UmlFieldData(NamedTuple):
    name:str

class UmlMethodParamData(NamedTuple):
    name:str

class UmlMethodData(NamedTuple):
    name:str
    params:list[UmlMethodParamData]
        

class UmlClassData(NamedTuple):
    name:str
    fields:list[UmlFieldData]
    methods:list[UmlMethodData]

class UmlRelationshipData(NamedTuple):
    relation_type:str
    source:str
    destination:str

class UmlProjectData(NamedTuple):
    classes:list[UmlClassData]
    relationships:list[UmlRelationshipData]


@dataclass
class UmlView(Protocol):

    def prompt_user(self, prompt:str) -> bool:
        """Shown directly to the user for additional information."""

    def get_user_input(self, text:str) -> str:
        """Shown directly to the user for additional information."""

    def get_user_command(self) -> list:
        """Runs view loop, waiting for user input or action."""

    def handle_exceptions(self, error_text:str):
        """"""

    def set_active_class(self, name:str):
        """"""

    @property
    def active_class(self) -> str:
        """"""

    def set_active_method(self, name:str, arity:int):
        """"""

    @property
    def active_method(self) -> tuple[str, int]:
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