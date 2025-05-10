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
    
    @abstractmethod
    def anchors(self) -> list[tuple[int, int]]:
        """Returns anchor points for the boundry object in which arrows can path
        to and from."""

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
        r1l, r1t = (self.x, self.y)
        r1r, r1b = (self.x+self.width, self.y+self.height)

        r2l, r2t = (elem.x, elem.y)
        r2r, r2b = (elem.x+elem.width, elem.y+elem.height)

        retval = not (r2l > r1r or r2r < r1l or r2t > r1b or r2b < r1t)

        return retval

    def anchors(self) -> list[tuple[int, int]]:
        """Returns anchor points for the boundry object in which arrows can path
        to and from. (left, top, right, bottom)"""
        
        x1, x2 = math.floor(self.x), math.floor(self.x + self.width)
        y1, y2 = math.floor(self.y), math.floor(self.y + self.height)
        mid_x = math.floor(self.x + (self.width * .5))
        mid_y = math.floor(self.y + (self.height * .5))

        top = (mid_x, y1)
        bottom = (mid_x, y2)
        left = (x1, mid_y)
        right = (x2, mid_y)

        return [left, top, right, bottom]

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
            if "px" not in value:
                raise Exception("font-size style value should be in pixels (px).")
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

class SvgInheritance(SvgElement):
    """"""

class SvgAggregation(SvgElement):
    """"""

class SvgComposition(SvgElement):
    """"""

class SvgRealization(SvgElement):
    """"""

class SvgTriangle(SvgElement):
    def __init__(self, points:tuple[tuple[int, int]], element_id:ElementId = "glyph", x:float=None, y:float=None):
        super().__init__(id, x, y)
        self.points = points

    @property
    def xml(self) -> str:
        """Get the element's xml."""
        return self.shape()

    @property
    def box_size(self) -> Boxsize:
        """Get the boxsize (width, height) of the element."""

    def shape(self) -> str:
        xml = '<polygon points="'
        for (x, y) in self.points:
            xml += '{x},{y} '.format(x=x, y=y)
        xml += '" fill="white" />\n'
        return xml

class SvgRelation(SvgElement):
    def __init__(self, element_id:ElementId, r1:SvgRect, r2:SvgRect, glyph_size:int = 5):
        super().__init__(element_id, 0, 0)
        self.r1 = r1
        self.r2 = r2
        self.glyph_size = glyph_size
        self.avoids:list[SvgBoundary] = []
        self.path:list[tuple[int, int]] = []
        self.use_path = False

    def set_path(self, path:list[tuple[int, int]]):
        self.path = path

    def path_xml(self) -> str:
        xml = ""
        if self.use_path:
            path = self.path.copy()
            xml = '<path d="'
            x1, y1 = path.pop(0)
            xml += f'M {x1},{y1} L'
            xml += ' '.join([f'{x},{y}' for x,y in path])
            xml += '" stroke="white" />'
        else:
            r1_anchors = self.r1.anchors()
            r2_anchors = self.r2.anchors()

            shortest_dist = float('inf')
            best_line = []
            for start in r1_anchors:
                for goal in r2_anchors:
                    dist = math.dist(start, goal)
                    if dist < shortest_dist:
                        best_line = [start, goal]
                    shortest_dist = min(dist, shortest_dist)

            (x1,y1), (x2,y2) = best_line            
            if (x2,y2) == r2_anchors[0]:
            # Left anchor
                points = (
                    (x2, y2),
                    (x2 - self.glyph_size, y2 - self.glyph_size),
                    (x2 - self.glyph_size, y2 + self.glyph_size)
                )
                x2 -= 1
            elif (x2,y2) == r2_anchors[1]:
            # Top anchor
                points = (
                    (x2, y2),
                    (x2 - self.glyph_size, y2 - self.glyph_size),
                    (x2 + self.glyph_size, y2 - self.glyph_size),
                )
                y2 -= 1
            elif (x2,y2) == r2_anchors[2]:
            # Right anchor
                points = (
                    (x2, y2),
                    (x2 + self.glyph_size, y2 - self.glyph_size),
                    (x2 + self.glyph_size, y2 + self.glyph_size)
                )
                x2 += 1
            else:
            # Bottom anchor
                points = (
                    (x2, y2,),
                    (x2 - self.glyph_size, y2 + self.glyph_size),
                    (x2 + self.glyph_size, y2 + self.glyph_size),
                )
                y2 += 1

            glyph = SvgTriangle(points)

            xml = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="white" />'
            xml += '\n' + glyph.xml

        return xml


    @property
    def xml(self) -> str:
        """"""
        return self.path_xml()
        # return self.path_xml() + self.line_glyph()
        # return self.line_xml() + self.line_glyph()
        # return self.line_xml()

    def line_vector(self) -> tuple[tuple[int,int]]:
        points = []
        p1_x = self.r1.x + math.floor(self.r1.w * .5)
        p1_y = self.r1.y + self.r1.h

        p2_x = self.r2.x + math.floor(self.r2.w * .5)
        p2_y = self.r2.y

        points.append((p1_x, p1_y,))

        p_x:int
        p_y:int


        points.append((p2_x,p2_y-self.glyph_size,))

        return((p1_x, p1_y,), (p2_x,p2_y-self.glyph_size,),)

    def line_glyph(self) -> str:
        # (_,_), (x,y) = self.line_vector()
        (x,y) = self.path[-1]
        points = (
            (x - self.glyph_size, y,),
            (x + self.glyph_size, y,),
            (x, y + self.glyph_size),
        )

        glyph = SvgTriangle(points)

        return glyph.xml

    def line_xml(self) -> str:
        (p1_x, p1_y), (p2_x, p2_y) = self.line_vector()
        xml = '<path d="'

        # Draw the line
        xml += 'M {x},{y} '.format(x=p1_x, y=p1_y)

        for j in range(p1_y, p2_y+1):
            intersection = False
            # print(i,j)
            p = SvgElement(-1, p1_x, j)
            for e in self.avoids:
                intersection = e.intersects(p)
                if intersection:
                    xml += 'l 0,{y} '.format(y=p.y - p1_y - 2)
                    dy = (e.h + e.y) + 2
                    
                    xml += 'H {x} '.format(x=e.x - 2)
                    xml += 'V {y} '.format(y=dy)
                    xml += 'H {x}'.format(x=p1_x)
                    
                    # xml += 'l {x},0 l 0,{y} l {x2},0 l 0,{y2} '.format(x=dx, y=dy, x2=-dx, y2=dy2)
                    break
            
            if intersection:
                break

        # xml += 'L {x},{y} '.format(x=p2_x, y=p2_y)

        xml += 'V {y}" '.format(y=p2_y)
        xml += 'stroke="white" stroke-dasharray="5,5" fill="none" />\n'
        return xml

    def avoid(self, elem:SvgElement):
        self.avoids.append(elem)

    @property
    def box_size(self) -> Boxsize:
        """Get the boxsize (width, height) of the element."""
        return None