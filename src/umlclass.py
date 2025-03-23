# Filename: umlclass.py
# Authors: Kyle Kalbach, Steven Barnes, Evan Magill, 
# Date: 2025-03-22
# Description: umlclass classes
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
    class_methods:dict[str, dict[str, UmlMethod]] = field(default_factory= lambda: {})

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
    
    def _overload_exists(self, method:UmlMethod) -> bool:
        """Checks if the method name and overloadID combination already exists on the UmlClass."""
        return method.name in self.class_methods.keys() and method.overloadID in self.class_methods.get(method.name).keys()

    def add_method(self, name:str, return_type:str, params:list[tuple[str, str]]) -> int:
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
        errors.valid_name(return_type)
        
        uml_method = UmlMethod(name, return_type, [])
        uml_method.add_parameters(params)

        if self._overload_exists(uml_method):
            raise errors.DuplicateMethodOverloadException()

        if self.class_methods.get(name) is None:
            self.class_methods[name] = {}

        self.class_methods.get(name)[uml_method.overloadID] = uml_method

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
        #TODO
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
        #TODO
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
    
    def add_parameter(self, methodname:str, arity:int, parameter:str):
        """Add a parameter to a specific method overload.

        Params:
            methodname: name of the method to add to
            arity: the method overload to add to
            parmaeter: the name of the new parameter being added
        Returns:

        Exceptions:
            MethodOverloadNotExistsException
            DuplicateMethodOverloadException
        """
        if not self._overload_exists(methodname, arity):
            raise errors.MethodOverloadNotExistsException()
        
        if self._overload_exists(methodname, arity + 1):
            raise errors.DuplicateMethodOverloadException()
        
        uml_method = self.class_methods.get(methodname).get(arity)
        uml_method.add_parameter(parameter)

        self.class_methods.get(methodname).pop(arity)
        self.class_methods.get(methodname)[len(uml_method.params)] = uml_method
        
    def rename_parameter(self, methodname:str, arity:int, oldname:str, newname:str):
        """Rename a parameter on a specific method overload.

        Params:
            methodname: name of the method
            arity: the method overload
            oldname: the name of the parameter to rename
            newname: the new name for the parameter
        Returns:

        Exceptions:
            MethodOverloadNotExistsException
            DuplicateMethodOverloadException
        """
        if not self._overload_exists(methodname, arity):
            raise errors.MethodOverloadNotExistsException()
        
        uml_method = self.class_methods.get(methodname).get(arity)
        uml_method.rename_parameter(oldname, newname)

    def remove_parameter(self, methodname:str, arity:int, parameter:str):
        """Remove a parameter from a specific method overload.

        Params:
            methodname: name of the method
            arity: the method overload
            oldname: the name of the parameter to remove
        Returns:

        Exceptions:
            MethodOverloadNotExistsException
            DuplicateMethodOverloadException
        """
        if not self._overload_exists(methodname, arity):
            raise errors.MethodOverloadNotExistsException()
        
        if self._overload_exists(methodname, arity - 1):
            raise errors.DuplicateMethodOverloadException()
        
        uml_method = self.class_methods.get(methodname).get(arity)
        uml_method.remove_parameter(parameter)

        self.class_methods.get(methodname).pop(arity)
        self.class_methods.get(methodname)[len(uml_method.params)] = uml_method

    def remove_all_parameters(self, methodname:str, arity:int):
        """Remove all parameters from a specific method overload.

        Params:
            methodname: name of the method
            arity: the method overload
        Returns:

        Exceptions:
            MethodOverloadNotExistsException
            DuplicateMethodOverloadException
        """
        if not self._overload_exists(methodname, arity):
            raise errors.MethodOverloadNotExistsException()

        if self._overload_exists(methodname, 0):
            raise errors.DuplicateMethodOverloadException()

        uml_method = self.class_methods.get(methodname).get(arity)
        uml_method.clear_parameters()

        self.class_methods.get(methodname).pop(arity)
        self.class_methods.get(methodname)[len(uml_method.params)] = uml_method

    def replace_all_parameters(self, methodname:str, arity:int, parameters:list[str]):
        """Replace all parameters from a specific method overload with new parameters.

        Params:
            methodname: name of the method
            arity: the method overload
            parameters: list of new parameter names
        Returns:

        Exceptions:
            MethodOverloadNotExistsException
            DuplicateMethodOverloadException
        """
        if not self._overload_exists(methodname, arity):
            raise errors.MethodOverloadNotExistsException()

        if self._overload_exists(methodname, len(parameters)):
            raise errors.DuplicateMethodOverloadException()
        
        uml_method = self.class_methods.get(methodname).get(arity)
        uml_method.replace_parameters(parameters)

        self.class_methods.get(methodname).pop(arity)
        self.class_methods.get(methodname)[len(uml_method.params)] = uml_method


    def to_dict(self) -> dict:
        methods = []
        for method in self.class_methods.values():
            methods.extend(method.values())
        return {
            'name': self.class_name,
            'fields': [f.to_dict() for f in self.class_fields.values()],
            'methods': [m.to_dict() for m in methods]
        }
        
        