# Filename: uml_svg_builder.py
# Authors: Steven Barnes
# Date: 2025-04-19
# Description: Code relating to SVG generation of a UmlProject.

from abc import ABC, abstractmethod
import math

from utilities import svg
from utilities.model_utils import UmlClassNT, UmlModelNT
from utilities.pathing_search import AStar


class SvgBuilder(ABC):
    """Builder interface for building a UML Diagram from a UmlProject."""

    @property
    @abstractmethod
    def svg(self) -> None:
        """Method to retreive the SVG."""

    @abstractmethod
    def produce_svg_part(self) -> None:
        """Method to generate the SVG component."""
    
    @abstractmethod
    def reset(self) -> None:
        """Method to reset the state of the builder."""

class UmlClassSvgBuilder(SvgBuilder):
    """SvgBuilder for building a UmlClass into a SVG element."""

    def __init__(self, umlclass: UmlClassNT, image: svg.SvgImage):
        self.umlclass = umlclass
        self.image = image
        self._xml = ""
        self.x = umlclass.x
        self.y = umlclass.y
        self.padding_y:float = 2.5
        self.padding_x:float = 5.0
        self.width = 0
        self.height = 0

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
            self.umlclass.name, self.x, self.y, 0, 0
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
        self.name.add_style("stroke", "solid 1px black")
        self.name.add_style("text-anchor", "middle")
        self.name.add_style("text-rendering", "optimizeLegibility")
        self.image.add(self.name)

        # Create field text elements
        for i, f in enumerate(self.umlclass.fields):
            f_text = svg.SvgText(
                f"+{f.name}:{f.type}", f"{self.umlclass.name}-field-{i}", 0, 0
            )
            f_text.add_style("font-size", "10px")
            f_text.add_style("fill", "red")
            f_text.add_style("text-rendering", "optimizeLegibility")
            self.fields.append(f_text)
            self.image.add(f_text)

        # Create method text elements
        for i, m in enumerate(self.umlclass.methods):
            m_text = svg.SvgText(
                f"-{m.name}({','.join(p.type for p in m.params)}):{m.return_type}",
                f"{self.umlclass.name}-method-{i}",
                0,
                0,
            )
            m_text.add_style("font-size", "10px")
            m_text.add_style("fill", "red")
            m_text.add_style("text-rendering", "optimizeLegibility")
            self.methods.append(m_text)
            self.image.add(m_text)

        self._set_required_size()

        # Close the group container
        self._xml = "</g>"

    def reset(self) -> None:
        """Method to reset the state of the builder."""
        if self.name:
            text_elements = [self.name, self.rect]
            text_elements.extend(self.fields)
            text_elements.extend(self.methods)
            list(map(self.image.elements.remove, text_elements))
            self.name = None
            self.fields.clear()
            self.methods.clear()
        
        self.width = 0
        self.height = 0

    def _set_required_size(self) -> None:
        """Sets the required width and height for the UmlClass rect and x and y 
        for text elements."""
        text_elements = [self.name]
        text_elements.extend(self.fields)
        text_elements.extend(self.methods)

        for e in text_elements:
            self.width = max(self.width, e.box_size.width)
            self.height += e.box_size.height

        # Set final height and width with appropriate padding.
        # Height adds an extra padding to account for the missed space between
        # the top of the rect and the UmlClass name text element.
        self.height += self.padding_y * (len(text_elements) + 2)
        self.width += self.padding_x * 2

        self.rect.width = self.width
        self.rect.height = self.height

        # Center the UmlClass name inside the rect
        self.name_x_offset = self.width * .5
        self.name.x = self.rect.x + self.name_x_offset
        self.name.y = self.rect.y + self.name_y_offset

        offset_y = self.name.y + self.name.box_size.height + self.padding_y
        for f in self.fields:
            f.x = self.rect.x + self.field_x_offset
            f.y = offset_y
            offset_y += f.box_size.height + self.padding_y
        
        for m in self.methods:
            m.x = self.rect.x + self.field_x_offset
            m.y = offset_y
            offset_y += m.box_size.height + self.padding_y

class UmlRelationshipBuilder(SvgBuilder):
    def __init__(self, image:svg.SvgImage, source:UmlClassSvgBuilder, dest:UmlClassSvgBuilder):
        """"""
        self.image = image
        self.source = source
        self.dest = dest
        self.box_buffer = 5

        self.relation:svg.SvgRelation = None

    @property
    def svg(self) -> None:
        """Method to retreive the SVG."""

    def produce_svg_part(self) -> None:
        """Method to generate the SVG component."""
        elem_id = f"r-{self.source.name.text}-{self.dest.name.text}"
        rect1 = self.source.rect
        rect2 = self.dest.rect

        # r1d = (
        #     math.floor(rect1.x - self.box_buffer),
        #     math.floor(rect1.y - self.box_buffer),
        #     math.floor(rect1.width + self.box_buffer),
        #     math.floor(rect1.height + self.box_buffer)
        # )

        # r2d = (
        #     math.floor(rect2.x - self.box_buffer),
        #     math.floor(rect2.y - self.box_buffer),
        #     math.floor(rect2.width + (self.box_buffer * 1)),
        #     math.floor(rect2.height + (self.box_buffer * 1))
        # )

        # new_rect1 = svg.SvgRect(None, *r1d)
        # new_rect2 = svg.SvgRect(None, *r2d)

        # search = AStar(self.grid, new_rect1.anchors(), new_rect2.anchors())

        # path = search.get_optimal_path()

        self.relation = svg.SvgRelation(elem_id, rect1, rect2)
        # self.relation.set_path(path)

        self.image.add(self.relation)

    def set_grid(self, grid:list[list[int]]):
        self.grid = grid

    def reset(self) -> None:
        """Method to reset the state of the builder."""

class UmlDiagramSvgBuilder(SvgBuilder):
    """SvgBuilder for building a UML Diagram into a SVG element."""
    def __init__(self, model:UmlModelNT):
        self.model = model
        self.image = svg.SvgImage(0,0)
        self.class_builders:list[UmlClassSvgBuilder] = []
        self.class_builder_map:dict[str, UmlClassSvgBuilder] = {}
        self.relation_builders:list[UmlRelationshipBuilder] = []
        self.padding = 50
        self.border_padding = 5
        self.box_buffer = 5

        for c in model.classes:
            builder = UmlClassSvgBuilder(c, self.image)
            builder.x = max(c.x, self.border_padding)
            builder.y = max(c.y, self.border_padding)
            self.class_builders.append(builder)
            self.class_builder_map[c.name] = builder

        for r in model.relationships:
            source = self.class_builder_map.get(r.source)
            dest = self.class_builder_map.get(r.destination)
            builder = UmlRelationshipBuilder(self.image, source, dest)
            self.relation_builders.append(builder)

    @property
    def svg(self) -> None:
        """Method to retreive the SVG."""

    def produce_svg_part(self) -> None:
        """Method to generate the SVG component."""
        width = 0
        height = 0

        for builder in self.class_builders:
            builder.produce_svg_part()

        self._handle_element_collisions()

        # Calculate final image size
        for builder in self.class_builders:
            width = max(width, builder.x + builder.width)
            height = max(height, builder.y + builder.height)

        self.image.width = width + self.border_padding
        self.image.height = height + self.border_padding

        grid = [[0 for _ in range(math.ceil(self.image.width))] for _ in range(math.ceil(self.image.height))]

        for builder in self.class_builders:
            rect1 = builder.rect

            r1d = (
                math.floor(rect1.x - self.box_buffer),
                math.floor(rect1.y - self.box_buffer),
                math.floor(rect1.width + self.box_buffer),
                math.floor(rect1.height + self.box_buffer)
            )

            new_rect1 = svg.SvgRect(None, *r1d)

            for i in range(new_rect1.y, new_rect1.y + new_rect1.height):
                for j in range(new_rect1.x, new_rect1.x + new_rect1.width):
                    grid[i][j] = 1

        for builder in self.relation_builders:
            builder.set_grid(grid)
            builder.produce_svg_part()
    
    def reset(self) -> None:
        """"""
    
    def _handle_element_collisions(self):
        builders = self.class_builders.copy()
        builders.sort(key=lambda b: b.x)
        for i in range(len(builders)):
            builder = builders[i]
            for j in range(len(builders)):
                if j != i:
                    b = builders[j]
                    if b.rect.intersects(builder.rect):
                        b.x = builder.x + builder.width + self.padding
                        b.reset()
                        b.produce_svg_part()

