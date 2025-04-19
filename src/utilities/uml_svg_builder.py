# Filename: uml_svg_builder.py
# Authors: Steven Barnes
# Date: 2025-04-19
# Description: Code relating to SVG generation of a UmlProject.

from abc import ABC, abstractmethod

from utilities import svg
from utilities.model_utils import UmlClassNamedTupledEncoder

UmlClass = UmlClassNamedTupledEncoder.UmlClassNT

class SvgBuilder(ABC):
    """Builder interface for building a UML Diagram from a UmlProject."""

    @property
    @abstractmethod
    def svg(self) -> None:
        """Method to retreive the SVG."""

    @abstractmethod
    def produce_svg_part(self) -> None:
        """Method to generate the SVG component."""

class UmlClassSvgBuilder(SvgBuilder):
    """SvgBuilder for building a UmlClass into a SVG element."""

    def __init__(self, umlclass: UmlClass, image: svg.SvgImage):
        self.umlclass = umlclass
        self.image = image
        self._xml = ""
        self.x = 0
        self.y = 0
        self.padding_y:float = 5.0
        self.padding_x:float = 5.0
        self.width = 0
        self.height = 0
        self.anchors = {
            "left": (
                0,
                0,
            ),
            "right": (
                0,
                0,
            ),
            "top": (
                0,
                0,
            ),
            "bottom": (
                0,
                0,
            ),
        }

        self.name_x_offset: float = 0.0
        self.name_y_offset: float = self.padding_y
        self.field_x_offset: float = self.padding_x
        self.field_y_offset: float = 0.0
        self.method_x_offset: float = self.padding_x
        self.method_y_offset: float = 0.0

        self.rect: svg.SvgRect = None
        self.name: svg.SvgText = None
        self.fields: list[svg.SvgText] = []
        self.methods: list[svg.SvgText] = []

    @property
    def svg(self) -> None:
        """Retreive the UmlClass xml."""

    def produce_svg_part(self) -> None:
        """Logic to create the UmlClass xml."""
        # Setup the group container
        self._xml = f'<g id="g-{self.umlclass.name}">'

        # Create the rect for the UmlClass
        self.rect = svg.SvgRect(
            self.umlclass.name, self.umlclass.x, self.umlclass.y, 0, 0
        )
        self.rect.add_style("stroke", "black")
        self.rect.add_style("stroke-width", "1")
        self.rect.add_style("fill", "none")
        self.image.add(self.rect)

        # Create the name text element
        self.name = svg.SvgText(self.umlclass.name, f"{self.umlclass.name}-name", 0, 0)
        self.name.add_style("font-size", "14px")
        self.name.add_style("font-weight", "bold")
        self.name.add_style("fill", "red")
        self.name.add_style("stroke", "solid 1px red")
        self.name.add_style("text-anchor", "middle")
        self.name.add_style("text-rendering", "optimizeLegibility")
        self.image.add(self.name)

        # Create field text elements
        for i, f in enumerate(self.umlclass.fields):
            f_text = svg.SvgText(
                f"+{f.name}:{f.type}", f"{self.umlclass.name}-field-{i}", 0, 0
            )
            self.fields.append(f_text)

        # Create method text elements
        for i, m in enumerate(self.umlclass.methods):
            m_text = svg.SvgText(
                f"-{m.name}({','.join(p.type for p in m.params)}):{m.return_type}",
                f"{self.umlclass.name}-method-{i}",
                0,
                0,
            )
            self.methods.append(m_text)

        self._set_required_size()

        # Close the group container
        self._xml = "</g>"

    def _set_required_size(self) -> None:
        """Sets the required width and height for the UmlClass rect and x and y 
        for text elements."""
        text_elements = [self.name]
        text_elements.extend(self.fields)
        text_elements.extend(self.methods)

        for e in text_elements:
            self.width = max(self.width, e.box_size.width)
            self.height = max(self.height, e.box_size.height)

        # Set final height and width with appropriate padding.
        # Height adds an extra padding to account for the missed space between
        # the top of the rect and the UmlClass name text element.
        self.height += self.padding_y * (len(text_elements) + 1)
        self.width += self.padding_x * 2

        self.rect.width = self.width
        self.rect.height = self.height

        self.name_x_offset = self.width * .5
        self.name.x = self.rect.x + self.name_x_offset
        self.name.y = self.rect.y + self.name_y_offset

        # offset_y = self.name.y + self.name.box_size.height + self.padding_y
        # for f in self.fields:
        #     f.x = self.rect.x + self.field_x_offset
        #     f.y = offset_y
        #     offset_y += f.box_size.height + self.padding_y