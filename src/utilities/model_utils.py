from typing import TypeVar, NamedTuple
from abc import ABC, abstractmethod
from umlmodel import UmlProject, UmlField, UmlParameter, UmlClass, UmlMethod, UmlRelationship, RelationshipType

T = TypeVar("T")

class DictDecoder(ABC):
    @abstractmethod
    def decode(self, data:dict) -> T:
        """"""

class UmlFieldDictDecoder(DictDecoder):

    def decode(self, data:dict) -> UmlField:
        """"""
        name = data.get("name")
        field_type = data.get("type")
        return UmlField(name, field_type)

class UmlParameterDictDecoder(DictDecoder):

    def decode(self, data:dict) -> UmlParameter:
        """"""
        name = data.get("name")
        param_type = data.get("type")
        return UmlParameter(name, param_type)

class UmlMethodDictDecoder(DictDecoder):

    def decode(self, data:dict) -> UmlMethod:
        """"""
        name = data.get("name")
        return_type = data.get("return_type")
        params = list(map(UmlParameterDictDecoder().decode, data.get("params")))
        return UmlMethod(name, return_type, params)

class UmlClassDictDecoder(DictDecoder):

    def decode(self, data:dict) -> UmlClass:
        """"""
        try:
            name = data.get("name")
            fields = list(map(UmlFieldDictDecoder().decode, data.get( "fields")))
            methods = list(map(UmlMethodDictDecoder().decode, data.get("methods")))
            # pos = data.get("position")
            # if pos:
            #     position = Position(pos.get("x"), pos.get("y"))
            # else:
            #     position = Position(0,0)
            retval = UmlClass(name, fields, methods)
            print(retval)
            return retval
        except Exception as e:
            print(e)
            raise e

class UmlRelationshipDictDecoder(DictDecoder):
    def __init__(self, classes:list[UmlClass]):
        self.classes = {c.class_name:c for c in classes}

    def decode(self, data:dict) -> UmlRelationship:
        source = data.get("source")
        source_class = self.classes.get(source)
        dest = data.get("destination")
        dest_class = self.classes.get(dest)
        rtype:str = data.get("type")
        rt = self.parse_type(rtype)
        return UmlRelationship(rt, source_class, dest_class)

    def parse_type(self, rtype:str) -> RelationshipType:
        d = {
            RelationshipType.AGGREGATION.name: RelationshipType.AGGREGATION,
            RelationshipType.COMPOSITION.name: RelationshipType.COMPOSITION,
            RelationshipType.INHERITANCE.name: RelationshipType.INHERITANCE,
            RelationshipType.REALIZATION.name: RelationshipType.REALIZATION
        }

        return d.get(rtype.upper())

class ModelDictDecoder(DictDecoder):
    
    def decode(self, data:dict) -> tuple[list[UmlClass], list[UmlRelationship]]:
        """"""
        classes = list(map(UmlClassDictDecoder().decode, data.get("classes")))
        relationships = list(map(UmlRelationshipDictDecoder(classes).decode, data.get("relationships")))
        return (classes,relationships,)

class DictEncoder:
    @abstractmethod
    def encode(self, o:T) -> dict:
        """"""

class UmlFieldDictEncoder:
    def encode(self, o:UmlField) -> dict:
        return {
            'name': o.name,
            'type': o.type
        }
    
class UmlParameterDictEncoder:
    def encode(self, o:UmlParameter) -> dict:
        return {
            'name': o.name,
            'type': o.type
        }
    
class UmlMethodDictEncoder:
    def encode(self, o:UmlMethod) -> dict:
        return {
            'name': o.name,
            'return_type': o.return_type,
            'params': list(map(UmlParameterDictEncoder().encode, o.params))
        }

class UmlClassDictEncoder:
    def encode(self, o:UmlClass) -> dict:
        """"""
        try:
            methods = []
            for m in o.class_methods.values():
                methods.append(m.values())
            retval = {
                'name': o.class_name,
                'fields': list(map(UmlFieldDictEncoder().encode, o.class_fields.values())),
                'methods': list(map(UmlMethodDictEncoder().encode, methods))
                # 'position': { 'x': o.position.x, 'y': o.position.y }
            }

            return retval
        except Exception as e:
            raise e

class UmlRelationshipDictEncoder:
    def encode(self, o:UmlRelationship) -> dict:
        return {
            'source': o.source_class.class_name,
            'destination': o.destination_class.class_name,
            'type': o.relationship_type.name.capitalize()
        }

class ModelDictEncoder:
    def encode(self, o:UmlProject) -> dict:
        """"""
        return {
            'classes': list(map(UmlClassDictEncoder().encode, o.classes.values())),
            'relationships': list(map(UmlRelationshipDictEncoder().encode, o.relationships))
        }

class NamedTupleEncoder:
    def encode(self, o:T) -> NamedTuple:
        """"""

class UmlFieldNT(NamedTuple):
    name:str
    type:str

class UmlFieldNamedTupledEncoder:

    def encode(self, o:UmlField) -> UmlFieldNT:
        return UmlFieldNT(o.name, o.type)

class UmlParameterNT(NamedTuple):
    name:str
    type:str

class UmlParameterNamedTupledEncoder:

    def encode(self, o:UmlParameter) -> UmlParameterNT:
        return UmlParameterNT(o.name, o.umltype)

class UmlMethodNT(NamedTuple):
    name:str
    return_type:str
    params:list[UmlParameterNT]

class UmlMethodNamedTupledEncoder:

    def encode(self, o:UmlMethod) -> UmlMethodNT:
        return UmlMethodNT(o.name, o.return_type, list(map(UmlParameterNamedTupledEncoder().encode, o.params)))

class UmlClassNT(NamedTuple):
    name:str
    fields:list[UmlFieldNT]
    methods:list[UmlMethodNT]
    x:float
    y:float

class UmlClassNamedTupledEncoder:

    def encode(self, o:UmlClass) -> UmlClassNT:
        """"""
        methods = []
        for m in o.class_methods.values():
            methods.extend(m.values())
        return UmlClassNT(
            o.class_name,
            list(map(UmlFieldNamedTupledEncoder().encode, o.class_fields.values())),
            list(map(UmlMethodNamedTupledEncoder().encode, methods)),
            o.class_pos_x,
            o.class_pos_y
        )

class UmlRelationshipNT(NamedTuple):
    source:str
    destination:str
    type:str

class UmlRelationshipNamedTupleEncoder:        
    def encode(self, o:UmlRelationship) -> UmlRelationshipNT:
        return UmlRelationshipNT(
            o.source_class.class_name,
            o.destination_class.class_name,
            o.relationship_type.name.capitalize()
        )

class UmlModelNT(NamedTuple):
    classes:list[UmlClassNT]
    relationships:list[UmlRelationshipNT]

class UmlModelNamedTupleEncoder:

    def encode(self, o:UmlProject) -> UmlModelNT:
        """"""
        return UmlModelNT(
            list(map(UmlClassNamedTupledEncoder().encode, o.classes.values())),
            list(map(UmlRelationshipNamedTupleEncoder().encode, o.relationships))
        )