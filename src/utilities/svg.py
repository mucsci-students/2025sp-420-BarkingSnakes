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

class SvgBoundary(SvgElement):
    """An SVG element which has a defined boundry and get check for intersections."""

    @abstractmethod
    def intersects(self, elem:SvgElement) -> bool:
        """Checks whether the provided element intersects with this element."""

class SvgRect(SvgBoundary):
    """A SVG rectangle element."""

    def __init__(self, element_id:ElementId, x:float, y:float, width:float, height:float):
        super().__init__(element_id, x, y)
        self.width = width
        self.height = height
        self.styles:dict[str, str] = {}
        self.classes:list[str] = []

    @property
    def xml(self) -> str:
        """Get the element's xml."""
        _xml = f'<rect x="{self.x}" y="{self.y}" width="{self.width}" height="{self.height}" '
        if self.element_id:
            _xml += f'id="{self.element_id}" '
        if self.classes:
            _xml += f'class="{" ".join(self.classes)}" '
        _xml += '/>'
        return _xml

    @property
    def box_size(self) -> Boxsize:
        """Get the boxsize (width, height) of the element."""
        return Boxsize(self.width, self.height)

    def intersects(self, elem:SvgElement) -> bool:
        """Checks whether the provided element intersects with this element."""
        min_x, min_y = (self.x, self.y)
        max_x, max_y = (self.x+self.width, self.y+self.height)
        intersect_x = elem.x >= min_x and elem.x <= max_x
        intersect_y = elem.y >= min_y and elem.y <= max_y
        return  intersect_x and intersect_y

class SvgText(SvgElement):
    """A SVG text element."""
    def __init__(self, text:str, element_id:ElementId, x:float, y:float):
        super().__init__(element_id, x, y)
        self.text = text
        self.font_size = 10
        self.scaling_magnitude = 10
        self.font_scale = 0.7

    @property
    def xml(self) -> str:
        """Get the element's xml."""
        adj_y = self.y + \
            (self.font_size * self.font_scale) + \
            (self.font_size / self.scaling_magnitude)

        _xml = f'<text x="{self.x}" y="{adj_y}" '
        if self.element_id:
            _xml += f'id="{self.element_id}" '
        if self.classes:
            _xml += f'class="{" ".join(self.classes)}" '

        _xml += f'>{self.text}</text>'
        return _xml

    def add_style(self, key, value):
        if key == "font-size":
            self.font_size = float(value.split("px")[0])
        return super().add_style(key, value)

    @property
    def box_size(self) -> Boxsize:
        """Get the boxsize (width, height) of the element."""
        return self._calc_text_boxsize()

    def _calc_text_boxsize(self) -> Boxsize:
        """Calculates the required width and height needed to render the text."""

        text = self.text
        h = math.ceil(self.font_size * self.font_scale)
        h = h + math.floor(h * .5)

        char_widths = {
            'a': 4.9, 'A': 7,
            'b': 5.1, 'B': 6,
            'c': 4.1, 'C': 7,
            'd': 5.4, 'D': 7,
            'e': 4.1, 'E': 6,
            'f': 4, 'F': 6,
            'g': 5, 'G': 8,
            'h': 5.2, 'H': 8,
            'i': 2.9, 'I': 4,
            'j': 2.5, 'J': 5,
            'k': 5.6, 'K': 8,
            'l': 2.8, 'L': 6,
            'm': 8.1, 'M': 10,
            'n': 5.2, 'N': 7,
            'o': 4.8, 'O': 8,
            'p': 5.1, 'P': 6,
            'q': 5.5, 'Q': 7.5,
            'r': 5.2, 'R': 8,
            's': 3.5, 'S': 5,
            't': 3.2, 'T': 7,
            'u': 5.2, 'U': 7,
            'v': 5, 'V': 7,
            'w': 7.2, 'W': 10,
            'x': 4.9, 'X': 7,
            'y': 5, 'Y': 7,
            'z': 4.1, 'Z': 7,
            ' ': 1, '0': 5,
            '1': 5, '2': 5,
            '3': 5, '4': 4.8,
            '5': 5, '6': 5,
            '7': 5, '8': 5,
            '9': 5, '(': 3.2,
            ')': 3, '+': 5.5,
            '-': 3, ':': 3,
            '_': 5.1
        }

        w = 0

        for c in text:
            w += self.font_size * (char_widths[c] / self.scaling_magnitude)
        return Boxsize(w, h)