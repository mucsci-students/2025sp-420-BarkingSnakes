# Filename: umlclass.py
# Authors: Kyle Kalbach, Steven Barnes, Evan Magill
# Date: 2025-02-25
# Description: umlclass methods
import logging
from dataclasses import dataclass, field
from umlfield import UmlField
from umlmethod import UmlMethod
import errors

@dataclass
class UmlClass:
    class_name:str
    class_fields:dict[str, UmlField] = field(default_factory= lambda: {})

    """ Method name is top level key and arity is lowest level key.
     e.g {'add': {0: <UmlMethod>, 2: <UmlMethod>}}
    """
    class_methods:dict[str, dict[int, UmlMethod]] = field(default_factory= lambda: {})

    def add_field(self,name:str) -> int:
        """
        Adds an field to the UmlClass
            Returns:
                0: if field added to the class
            Exceptions:
                DuplicateFieldError: if name exists
                InvalidNameError: if name invalid
        """ 
        if name in self.class_fields.keys():
            #return error code or handle existing key
            raise errors.DuplicateFieldException()
        errors.valid_name(name)
        self.class_fields[name] = UmlField(name)
        return 0

    def remove_field(self,name:str) -> int:
        """Removes an field from the UmlClass
        Params:
            name: name of the field to remove
        Returns:
            0: if the field was successfully removed
            a number corresponding to an error in the errors class
            if an field was not removed from the class
        """
        if name not in self.class_fields.keys():
            #return error code for nonexistent field
            raise errors.NoSuchObjectException(object_type="field")
        self.class_fields.pop(name)
        return 0
    
    def rename_field(self,oldname:str,newname:str) -> int:
        """Renames the specified field
        Params: 
            oldname: existing field to rename
            newname: name to replace oldname
        Returns:
            0: if the field was successfully renamed
        Exceptions:
            UMLException:InvalidNameError if the new name is invalid
            UMLException:NoSuchObjectError if the field does not exist
            UMLException:DuplicateFieldError if newname exist in class_fields
        """
        if oldname not in self.class_fields.keys():
            #return error code for nonexistent field
            raise errors.NoSuchObjectException(object_type="field")

        errors.valid_name(newname)

        if newname in self.class_fields.keys():
            #return error code or handle existing key
            raise errors.DuplicateFieldException()
        
        self.class_fields.pop(oldname)
        self.add_field(newname)
        return 0

    def rename_umlclass(self,name:str) -> int:
        """Renames the UmlClass

        Params:
            name: new name for the class  

        Returns:
            0: if the class was successfully renamed

        Exceptions:
            UMLException:InvalidNameError if the new name is invalid
            UMLException:NoSuchObjectError if the class does not exist
        """
        # method will throw exception for parent to catch 
        # if name is invalid
        errors.valid_name(name)
        self.class_name = name
        return 0
    
    def _overload_exists(self, name:str, arity:int) -> bool:
        """Checks if the method name and arity combination already exists on the UmlClass."""
        return name in self.class_methods.keys() and arity in self.class_methods.get(name).keys()

    def add_method(self, name:str, params:list[str]) -> int:
        """Adds a UmlMethod to the UmlClass

        Params:
            name: name for the method to add
            params: a list of parameter names attached to the method

        Returns:
            0 if the class was successfully renamed

        Exceptions:
            UMLException:InvalidNameError if the new name is invalid
            UMLException:NoSuchObjectError if the class does not exist
            DuplicateMethodOverloadException
        """

        errors.valid_name(name)
        if self._overload_exists(name, len(params)):
            raise errors.DuplicateMethodOverloadException()
        
        uml_method = UmlMethod(name, {})
        uml_method.add_parameters(params)

        if self.class_methods.get(name) is None:
            self.class_methods[name] = {}

        self.class_methods.get(name)[uml_method.arity] = uml_method

        return 0 

    def rename_method(self, name:str, arity:int, newname:str) -> int:
        """Rename a UmlMethod to the UmlClass

        Params:
            name: name for the method to add
            newname: new name to change the method to

        Returns:
            0 if the method was successfully renamed

        Exceptions:
            UMLException:InvalidNameError if the new name is invalid
            DuplicateMethodOverloadException:
            MethodOverloadNotExistsException:
        """
        if not self.class_methods.get(name):
            raise errors.MethodNameNotExistsException()

        if self._overload_exists(newname, arity):
            raise errors.DuplicateMethodOverloadException()


        if self._overload_exists(name, arity):
            uml_method = self.class_methods.get(name).get(arity)

            # add_method handles logic of checking in class_method for missing
            # top level keys and handles name validation
            self.add_method(newname, [p for p in uml_method.params.keys()])

            return self.remove_method(name, arity)

        raise errors.MethodOverloadNotExistsException()
        
    def remove_method(self, name:str, arity:int) -> int:
        """Remove a UmlMethod from the UmlClass

        Params:
            name: name for the method to remove
            arity: arity of the overload

        Returns:
            0 if the method was successfully renamed

        Exceptions:
            MethodNameNotExistsException:
            MethodOverloadNotExistsException:
        """
        if not self.class_methods.get(name):
            raise errors.MethodNameNotExistsException()

        if self._overload_exists(name, arity):
            self.class_methods.get(name).pop(arity)

            if not any(self.class_methods.get(name)):
                self.class_methods.pop(name)
            
            return 0
        
        raise errors.MethodOverloadNotExistsException()

    def remove_all_methods(self) -> int:
        """Remove all UmlMethods from the UmlClass

        Params:

        Returns:
            0 if all methods were successfully removed

        Exceptions:
        """
        self.class_methods.clear()

    def remove_all_overloads(self, name:str) -> int:
        """Remove all overloads of the specified name from the UmlClass

        Params:
            name: name of the method to remove
        Returns:
            0 if all method overloads were sucessfully removed

        Exceptions:
            MethodNameNotExistsException:
        """
        if not self.class_methods.get(name):
            raise errors.MethodNameNotExistsException()
        
        self.class_methods.pop(name)
        return 0
        
        