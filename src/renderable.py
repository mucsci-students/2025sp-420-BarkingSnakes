from typing import Protocol


class Renderable(Protocol):
    def render(self):
        """"""