# Filename: umlrelationship.py
# Authors: Evan Magill, Steven Barnes, Juliana Vinluan
# Date: 2025-03-07
# Description: Class encapsulating umlrelationships
import logging
import errors
from dataclasses import dataclass
from enum import Enum
from umlclass import UmlClass

class RelationshipType(Enum):
    DEFAULT = 0
    AGGREGATION = 1
    COMPOSITION = 2
    INHERITANCE = 3
    REALIZATION = 4

@dataclass
class UmlRelationship:
    relationship_type:RelationshipType
    source_class:UmlClass
    destination_class:UmlClass

    def __eq__(self, other):
        """
        Checks equality between UmlRelationships.
        UmlRelationships of the DEFAULT RelationshipType are considered symmetric, so equality still holds if source and destination are switched.
        """
        if self.relationship_type != other.relationship_type:
            return False
        if self.source_class == other.source_class and self.destination_class == other.destination_class:
            return True # All fields are equal.
        if (self.relationship_type == RelationshipType.DEFAULT
                and self.source_class == other.destination_class
                and self.destination_class == other.source_class):
            return True # source and destination are swapped for other, but is equal for DEFAULT relationship type.
        return False
    
    def __hash__(self):
        """
        Produces a hashed value such that UmlRelationships considered equal by __eq__ will produce the same hash value.
        """
        # id() is unique to one currently existing object. Appropriate to capture reference to specific UmlClass regardless of that class's properties.
        if self.relationship_type == RelationshipType.DEFAULT:
            # A DEFAULT type relationship is symmetric. Produces same hash regardless of source, destination ordering.
            # Hash the result to keep typical scale of hashed value.
            return hash(id(self.source_class) + id(self.destination_class))
        # If relationship type is not default, scale source and destination id()s by different amounts to avoid collision.
        # Hash the result to keep typical scale of hashed value.
        return hash(hash(self.relationship_type) + 3 * id(self.source_class) + 5 * id(self.destination_class))
    
    def __str__(self):
        arrow = " -----------> "
        
        match self.relationship_type:
            case RelationshipType.AGGREGATION:
                arrow = " ---------< > "
            case RelationshipType.COMPOSITION:
                arrow = " ---------<#> "
            case RelationshipType.INHERITANCE:
                arrow = " ----------|> "
            case RelationshipType.REALIZATION:
                arrow = " -- -- -- -|> "

        return self.source_class.class_name + " -> " + self.destination_class.class_name