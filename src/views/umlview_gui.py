from dataclasses import dataclass
from flask import g

from view import View
from renderable import Renderable
from gui.renderables import UmlClassListRenderable

@dataclass
class UmlGuiView(View):
    """"""
    command:str = ""
    renderable:Renderable = None
    _active_class:str = None

    def render(self, renderable:Renderable):
        self.renderable = renderable

    def get_user_command(self) -> list[str]:
        """"""
        print("[View]Waiting for a command from flask.")
        while self.command == "":
            True
        print("Got command: ", self.command)
        return self.command.split()
        

    def set_command(self, command:str):
        """"""
        self.command = command

    def get_renderable(self) -> Renderable:
        """"""
        return self.renderable
    
    def set_active_class(self, name:str):
        """"""
        self._active_class = name

    @property
    def active_class(self) -> str:
        """"""
        return self._active_class