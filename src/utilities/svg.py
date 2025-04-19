# Filename: svg.py
# Authors: Steven Barnes
# Date: 2025-04-19
# Description: Code relating to SVG generation of a UmlProject.

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union, NamedTuple
import math

ElementId = Union[str, int]

class Boxsize(NamedTuple):
    """Stores the width and height values."""
    width:float
    height:float

class SvgImage:
    r"""An SVG image (\<svg\> tag)."""
    def __init__(self, width:float, height:float):
        self.width = width
        self.height = height
        self.xmlns = "http://www.w3.org/2000/svg"
        self.elements:list[SvgElement] = []

    @property
    def xml(self) -> str:
        """Get the image xml."""
        _xml = f'<svg width="{self.width}" height="{self.height}" xmlns="{self.xmlns}" >\n'
        _xml += self._get_styles()
        _xml += '\n'.join([e.xml for e in self.elements]) + "\n"
        _xml += "</svg>"
        return _xml

    def add(self, elem:SvgElement):
        """Add the SvgElement to the image."""
        self.elements.append(elem)

    def _get_styles(self) -> str:
        """Iterators over all child elements and adds their styles using their ElementId"""
        def generate_element_style(e:SvgElement) -> str:
            """Aggregate the elements styles together."""
            e_style = f'  #{e.element_id} ' + "{\n"
            e_style += '\n'.join(f'    {k}:{v};' for k,v in e.styles.items())
            e_style += "\n  }"
            return e_style

        styles = "<style>\n"
        styles += '\n'.join(generate_element_style(e) for e in self.elements) + "\n"
        styles += "</style>\n"
        return styles

class SvgElement(ABC):
    """Basic SVG element which others are derived."""

    def __init__(self, element_id:ElementId, x:float, y:float):
        """"""
        self.element_id = element_id
        self.x = x
        self.y = y
        self.parent:SvgImage = None
        self.styles:dict[str, str] = {}
        self.classes:list[str] = []

    @property
    @abstractmethod
    def xml(self) -> str:
        """Get the element's xml."""

    @property
    @abstractmethod
    def box_size(self) -> Boxsize:
        """Get the boxsize (width, height) of the element."""

    def add_class(self, name:str) -> None:
        """Adds a class to the elements class attribute."""
        self.classes.append(name)

    def add_style(self, key:str, value:str) -> None:
        """Adds a style to the element, or to the class if classname is provided."""
        self.styles[key] = value

    def set_parent(self, image:SvgImage) -> None:
        """Sets the parent svg image."""
        self.parent = image