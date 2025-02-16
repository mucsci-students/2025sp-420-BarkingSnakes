# Filename: umlrelationship.py
# Authors: Evan Magill, Steven Barnes
# Date: 2025-02-11
# Description: Class encapsulating umlrelationships
from dataclasses import dataclass
from enum import Enum
from umlclass import UmlClass

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
    
    def __hash__(self):
        if self.relationship_type == RelationshipType.DEFAULT:
            return hash(self.source_class) + hash(self.destination_class)
        return hash(self.relationship_type) + 3 * hash(self.source_class) + 5 * hash(self.destination_class)
    
    def __str__(self):
        return self.source_class.class_name + " -> " + self.destination_class.class_name