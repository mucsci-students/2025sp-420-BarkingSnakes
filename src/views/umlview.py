# Filename: umlview.py
# Authors: Steven Barnes, John Hershey, Evan Magill, Kyle Kalbach, Spencer Hoover, Juliana Vinluan
# Date: 2025-03-01
# Description: View (MVC) for UML program.

from dataclasses import dataclass
from typing import Protocol


class UmlFieldData:
    def __init__(self, name:str):
        self.name = name

class UmlMethodParamData:
    def __init__(self, name):
        self.name = name

class UmlMethodData:
    def __init__(self, name:str, params:list[UmlMethodParamData]):
        self.name = name
        self.params = params

class UmlClassData:
    def __init__(self, name:str, fields:list[UmlFieldData], methods:list[UmlMethodData]):
        """"""
        self.name = name
        self.fields = fields
        self.methods = methods

class UmlRelationshipData:
    def __init__(self, type:str, source:str, destination:str):
        self.type = type
        self.source = source
        self.destination = destination

class UmlProjectData:
    def __init__(self, classes: list[UmlClassData], relationships:list[UmlRelationshipData]):
        self.classes = classes
        self.relationships = relationships


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

    def set_active_method(self, name:str):
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