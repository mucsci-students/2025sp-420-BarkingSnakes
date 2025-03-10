from typing import Protocol
from dataclasses import dataclass

from renderable import Renderable

@dataclass
class View (Protocol):
    """"""
    
    def render(self, renderable:Renderable):
        """"""

    def get_user_command(self) -> list[str]:
        """"""
    
    def set_command(self, command:str):
        """"""
    
    def get_renderable(self) -> Renderable:
        """"""