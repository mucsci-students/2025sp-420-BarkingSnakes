# Filename: umlrelationship.py
# Authors: Evan Magill, Steven Barnes
# Date: 2025-02-11
# Description: Class encapsulating umlrelationships
import logging
from dataclasses import dataclasses
from umlclass import UmlClass
from enum import Enum
import errors

class RelationshipType(Enum):
    DEFAULT = 0

@dataclass
class UmlRelationship:
    relationship_type:RelationshipType
    source_class:UmlClass
    destination_class:UmlClass

    def __eq__(self, other):
        if self.relationship_type != other.relationship_type:
            return False
        if self.source_class == other.source_class and self.destination_class == other.destination_class:
            return True
        if (self.relationship_type == RelationshipType.DEFAULT
                and self.source_class == other.destination_class
                and self.destination_class == other.source_class):
            return True
        return False
    