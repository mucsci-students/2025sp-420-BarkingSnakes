from __future__ import annotations
import copy

from umlcommands.base_commands import UmlCommand, TypedCommand, CallbackCommand, CommandOutcome
from umlcontroller_observer import UmlControllerObserver
from umlclass import UmlClass, UmlMethod
from umlrelationship import UmlRelationship
import errors

class ControllerCommand(TypedCommand[UmlControllerObserver]):
    """A command specific for the UmlController."""

    __DRIVER_TYPE__ = UmlControllerObserver
    
    def raise_InvalidName(self, name:str, context:str):
        try:
            errors.valid_name(name)
        except errors.InvalidNameException as e:
            error_text = f"The {context} name {name} cannot be used as a {context} name."
            self.set_result(CommandOutcome.FAILED, e, error_text)
            raise e

class ActiveClassCommand(ControllerCommand):

    def raise_NoActiveClass(self):
        """Raises a NoActiveClassException if the controller isn't tracking an
        active class and sets the CommandResult accordingly."""
        if not self.driver.active_class:
            e = errors.NoActiveClassException()
            error_text = "This operation requires you to be in an active class context."
            self.set_result(CommandOutcome.FAILED, e, error_text)
            raise e

    @property
    def umlclass(self) -> UmlClass:
        return self.driver.active_class

class ActiveMethodCommand(ActiveClassCommand):

    def raise_NoActiveMethod(self):
        """Raises a NoActiveMethodException if the controller isn't tracking an
        active method and sets the CommandResult accordingly."""
        self.raise_NoActiveClass()
        if not self.driver.active_method:
            e = errors.NoActiveMethodException()
            error_text = "This operation requires you to be in an active method context."
            self.set_result(CommandOutcome.FAILED, e, error_text)
            raise e

    @property
    def umlmethod(self) -> UmlMethod:
        return self.driver.active_method

class BackCommand(ControllerCommand):
    def execute(self):
        if self.driver.active_method:
            self.driver.active_method = None
        elif self.driver.active_class:
            self.driver.active_class = None
        self.set_result(CommandOutcome.SUCCESS)

class ListClassesCommand(ControllerCommand):
    from umlclass import UmlClass
    def execute(self):
        if self.driver.active_class:
            self._classes = [self.driver.active_class]
        else:
            self._classes = list(self.driver.model.classes.values())
        self.set_result(CommandOutcome.SUCCESS)
    
    @property
    def umlclasses(self) -> list[UmlClass]:
        return self._classes

class ListRelationCommand(ControllerCommand):
    def execute(self):
        try:
            self._relationships = self.driver.model.relationships
            self.set_result(CommandOutcome.SUCCESS)
        except errors.UMLException as uml_e:
            self.set_result(CommandOutcome.FAILED, uml_e)
        except Exception as e:
            self.set_result(CommandOutcome.EXCEPTION, e)
    
    @property
    def relationships(self) -> set[UmlRelationship]:
        return self._relationships
        

class GetUmlClassCommand(ControllerCommand):
    from umlclass import UmlClass
    def execute(self):
        try:
            self._umlclass = self.driver.model.get_umlclass(self.name)
            self.driver.active_class = self.umlclass
            self.set_result(CommandOutcome.SUCCESS)
        except errors.UMLException as uml_e:
            self.set_result(CommandOutcome.FAILED, uml_e)
        except Exception as e:
            self.set_result(CommandOutcome.EXCEPTION, e)
    
    @property
    def name(self) -> str:
        return self._args[-1]
    
    @property
    def umlclass(self) -> UmlClass:
        return self._umlclass

class AddClassCommand(ControllerCommand):
    def execute(self):
        try:
            self.driver.model.add_umlclass(self.name)
            self.set_result(CommandOutcome.SUCCESS)
        except errors.InvalidNameException as name_ex:
            error_text = "The name provided cannot be used as a class name."
            self.set_result(CommandOutcome.FAILED, name_ex, error_text)
        except errors.UMLException as uml_e:
            self.set_result(CommandOutcome.FAILED, uml_e)
        except Exception as e:
            self.set_result(CommandOutcome.EXCEPTION, e)

    @property
    def name(self) -> str:
        return self._args[-1]

    @property
    def umlclass(self) -> UmlClass:
        return self.driver.model.get_umlclass(self.name)

class RenameClassCommand(ControllerCommand):
    def execute(self):
        """"""
        try:
            self.raise_NoActiveClass()
            self._umlclass = self.driver.active_class
            
            self._backup = copy.copy(self.umlclass)

            self.driver.model.classes.pop(self.umlclass.class_name)
            self.umlclass.rename_umlclass(self.newname)
        except errors.NoActiveClassException as nac_e:
            return
        except errors.InvalidNameException as name_ex:
            error_text = "The name provided cannot be used as a class name."
            self.set_result(CommandOutcome.FAILED, name_ex, error_text)
        except errors.UMLException as uml_e:
            self.set_result(CommandOutcome.FAILED, uml_e)
        except Exception as e:
            self.set_result(CommandOutcome.EXCEPTION, e)

        if self.get_result() is None:
            self.set_result(CommandOutcome.SUCCESS)
            self.driver.model.classes[self.umlclass.class_name] = self.umlclass
            self.driver.active_class = self.umlclass
        else:
            self.driver.model.classes[self._backup.class_name] = self._backup
    
    @property
    def newname(self) -> str:
        return self._args[-1]
    
    @property
    def umlclass(self) -> UmlClass:
        return self._umlclass

class DeleteClassCommand(ControllerCommand):
    def execute(self):
        try:
            self.raise_NoActiveClass()
            self.set_result(CommandOutcome.SUCCESS)
        except errors.NoActiveClassException as nac_e:
            return
        except errors.UMLException as uml_e:
            self.set_result(CommandOutcome.FAILED, uml_e)
        except Exception as e:
            self.set_result(CommandOutcome.EXCEPTION, e)

class AddFieldCommand(ActiveClassCommand):
    def execute(self):
        try:
            self.raise_NoActiveClass()
            self.raise_InvalidName(self.name, "field")
            self.raise_InvalidName(self.field_type, "field type")
         
            self.umlclass.add_field(self.name, self.field_type)
            self.set_result(CommandOutcome.SUCCESS)
        except errors.NoActiveClassException as nac_e:
            return
        except errors.InvalidNameException as name_ex:
            return
        except errors.UMLException as uml_e:
            self.set_result(CommandOutcome.FAILED, uml_e)
        except Exception as e:
            self.set_result(CommandOutcome.EXCEPTION, e)
    
    @property
    def name(self) -> str:
        prop_index = 2
        return self._args[prop_index]

    @property
    def field_type(self) -> str:
        prop_index = 3
        return self._args[prop_index]

class RenameFieldCommand(ActiveClassCommand):
    def execute(self):
        try:
            self.raise_NoActiveClass()
            self.raise_InvalidName(self.name, "field")
            self.raise_InvalidName(self.newname, "field")
            classname = self.driver.active_class.class_name
            self.driver.model.rename_field(classname, self.name, self.newname)
            self.set_result(CommandOutcome.SUCCESS)
        except errors.NoActiveClassException as nac_e:
            return
        except errors.NoSuchObjectException as nso_e:
            error_text = f"The field {self.name} does not exist on class {classname}."
            self.set_result(CommandOutcome.FAILED, nso_e, error_text)
        except errors.InvalidNameException as name_ex:
            return
        except errors.UMLException as uml_e:
            self.set_result(CommandOutcome.FAILED, uml_e)
        except Exception as e:
            self.set_result(CommandOutcome.EXCEPTION, e)

    @property
    def name(self) -> str:
        prop_index = 2
        return self._args[prop_index]

    @property
    def newname(self) -> str:
        prop_index = 3
        return self._args[prop_index]

class DeleteFieldCommand(ActiveClassCommand):
    def execute(self):
        try:
            self.raise_NoActiveClass()
            classname = self.driver.active_class.class_name
            self.driver.model.delete_field(classname, self.name)
            self.set_result(CommandOutcome.SUCCESS)
        except errors.NoActiveClassException as nac_e:
            return
        except errors.NoSuchObjectException as nso_e:
            error_text = f"The field {self.name} does not exist on class {classname}."
            self.set_result(CommandOutcome.FAILED, nso_e, error_text)
        except errors.UMLException as uml_e:
            self.set_result(CommandOutcome.FAILED, uml_e)
        except Exception as e:
            self.set_result(CommandOutcome.EXCEPTION, e)

    @property
    def name(self) -> str:
        return self._args[-1]

class MethodAddCommand(ActiveClassCommand):
    def execute(self):
        try:
            self.raise_NoActiveClass()
            self.raise_InvalidName(self.name, "method")
            self.raise_InvalidName(self.return_type, "return type")
            for p in self.params:
                param_name, param_type = p
                self.raise_InvalidName(param_name, "parameter")
                self.raise_InvalidName(param_type, "parameter type")

            classname = self.driver.active_class.class_name

            self.driver.model.add_method(classname, self.name, self.return_type, self.params)
            self.set_result(CommandOutcome.SUCCESS)
        except errors.NoActiveClassException as nac_e:
            return
        except errors.InvalidNameException as name_ex:
            return
        except errors.MethodNameNotExistsException as mnne_e:
            print(mnne_e.with_traceback())
        except errors.UMLException as uml_e:
            self.set_result(CommandOutcome.FAILED, uml_e)
        except Exception as e:
            self.set_result(CommandOutcome.EXCEPTION, e)        

    @property
    def name(self) -> str:
        prop_index = 2
        return self._args[prop_index]

    @property
    def return_type(self) -> str:
        prop_index = 3
        return self._args[prop_index]

    @property
    def params(self) -> list[tuple[str, str]]:
        prop_index = 4
        return [tuple(p.split(":")) for p in self._args[prop_index:]]

class MethodContextCommand(ActiveClassCommand):
    def execute(self):
        try:
            self.raise_NoActiveClass()
            classname = self.driver.active_class.class_name
            self._method = self.driver.model.get_umlmethod(classname, self.name, self.overloadI_id)
            self.driver.active_method = self.umlmethod
            self.set_result(CommandOutcome.SUCCESS)
        except errors.NoActiveClassException as nac_e:
            return
        except errors.MethodNameNotExistsException as mnne_e:
            error_text = f"The method {self.name} does not exist on the class {classname}."
            self.set_result(CommandOutcome.FAILED, mnne_e, error_text)
        except errors.MethodOverloadNotExistsException as mone_e:
            error_text = f"The method signature {self.overloadI_id} does not exists for method {self.name} on class {classname}."
            self.set_result(CommandOutcome.FAILED, mone_e, error_text)
        except errors.UMLException as uml_e:
            self.set_result(CommandOutcome.FAILED, uml_e)
        except Exception as e:
            self.set_result(CommandOutcome.EXCEPTION, e) 
    
    @property
    def name(self) -> str:
        prop_index = 1
        return self._args[prop_index]

    @property
    def overloadI_id(self) -> str:
        proper_index = 2
        return " ".join(self._args[2:])

    @property
    def umlmethod(self) -> UmlMethod:
        return self._method

class MethodDeleteCommand(ActiveClassCommand):
    def execute(self):
        try:
            self.raise_NoActiveClass()
            classname = self.umlclass.class_name
            methodname = self.name
            overload_id = self.overload_id
            self.driver.model.delete_method(classname, methodname, overload_id)
            if self.driver.active_method.name == methodname and self.driver.active_method.overloadID == overload_id:
                self.driver.active_method = None
            self.set_result(CommandOutcome.SUCCESS)
        except errors.NoActiveClassException as nac_e:
            return
        except errors.MethodNameNotExistsException as mnne_e:
            error_text = f"The method {self.name} does not exist on the class {classname}."
            self.set_result(CommandOutcome.FAILED, mnne_e, error_text)
        except errors.MethodOverloadNotExistsException as mone_e:
            error_text = f"The method signature {self.overload_id} does not exists for method {self.name} on class {classname}."
            self.set_result(CommandOutcome.FAILED, mone_e, error_text)
        except errors.UMLException as uml_e:
            self.set_result(CommandOutcome.FAILED, uml_e)
        except Exception as e:
            self.set_result(CommandOutcome.EXCEPTION, e)
    
    @property
    def name(self) -> str:
        prop_index = 2
        return self._args[prop_index]

    @property
    def overload_id(self) -> str:
        prop_index = 3
        return " ".join(self._args[prop_index:])

    @property
    def umlmethod(self) -> UmlMethod:
        return self.driver.active_method

class MethodRenameCommand(ActiveMethodCommand):
    def execute(self):
        try:
            self.raise_NoActiveMethod()
            self.raise_InvalidName(self.newname, "method")

            classname = self.umlclass.class_name
            methodname = self.umlmethod.name
            overload_id = self.umlmethod.overloadID
            self.driver.model.rename_method(classname, methodname, self.newname, overload_id)
            self.driver.active_method = self.driver.model.get_umlmethod(classname, self.newname, overload_id)
            self.set_result(CommandOutcome.SUCCESS)
        except errors.NoActiveClassException as nac_e:
            return
        except errors.NoActiveMethodException as nam_e:
            return
        except errors.InvalidNameException as name_e:
            return
        except errors.MethodNameNotExistsException as mnne_e:
            error_text = f"The method {self.name} does not exist on the class {classname}."
            self.set_result(CommandOutcome.FAILED, mnne_e, error_text)
        except errors.MethodOverloadNotExistsException as mone_e:
            error_text = f"The method signature {self.overload_id} does not exists for method {self.name} on class {classname}."
            self.set_result(CommandOutcome.FAILED, mone_e, error_text)
        except errors.UMLException as uml_e:
            self.set_result(CommandOutcome.FAILED, uml_e)
        except Exception as e:
            self.set_result(CommandOutcome.EXCEPTION, e)

    @property
    def newname(self) -> str:
        prop_index = 2
        return self._args[prop_index]

class ParameterAddCommand(ActiveMethodCommand):
    def execute(self):
        try:
            self.raise_NoActiveMethod()
            self.raise_InvalidName(self.name, "parameter")
            self.raise_InvalidName(self.param_type, "parameter type")

            classname = self.umlclass.class_name
            methodname = self.umlmethod.name
            overload_id = self.umlmethod.overloadID
            self.driver.model.add_parameter(classname, methodname, overload_id, self.name, self.param_type)
            self.set_result(CommandOutcome.SUCCESS)
        except errors.NoActiveClassException:
            return
        except errors.NoActiveMethodException:
            return
        except errors.InvalidNameException:
            return
        except errors.DuplicateMethodOverloadException as dmo_e:
            error_text = f"The resulting method signature already exists on the class {classname}."
            self.set_result(CommandOutcome.FAILED, dmo_e, error_text)
        except errors.UMLException as uml_e:
            self.set_result(CommandOutcome.FAILED, uml_e)
        except Exception as e:
            self.set_result(CommandOutcome.EXCEPTION, e)
    
    @property
    def name(self) -> str:
        prop_index = 2
        return self._args[prop_index]
    
    @property
    def param_type(self) -> str:
        prop_index = 3
        return self._args[prop_index]

class ParameterRenameCommand(ActiveMethodCommand):
    def execute(self):
        try:
            self.raise_NoActiveMethod()
            self.raise_InvalidName(self.name, "parameter")
            self.raise_InvalidName(self.newname, "parameter")

            classname = self.umlclass.class_name
            methodname = self.umlmethod.name
            overload_id = self.umlmethod.overloadID

            self.driver.model.rename_parameter(classname, methodname, overload_id, self.name, self.newname)
            self.set_result(CommandOutcome.SUCCESS)
        except errors.NoActiveClassException:
            return
        except errors.NoActiveMethodException:
            return
        except errors.InvalidNameException:
            return
        except errors.DuplicateParameterException as dp_e:
            error_text = f"A parameter named {self.newname} in method {methodname} ({overload_id}) on class {classname} already exists."
            self.set_result(CommandOutcome.FAILED, dp_e, error_text)
        except errors.NoSuchParameterException as nsp_e:
            error_text = f"No parameter named {self.name} in method {methodname} ({overload_id}) on class {classname} exists."
            self.set_result(CommandOutcome.FAILED, nsp_e, error_text)
        except errors.UMLException as uml_e:
            self.set_result(CommandOutcome.FAILED, uml_e)
        except Exception as e:
            self.set_result(CommandOutcome.EXCEPTION, e)

    @property
    def name(self) -> str:
        prop_index = 2
        return self._args[prop_index]
    
    @property
    def newname(self) -> str:
        prop_index = 3
        return self._args[prop_index]

class ParameterDeleteCommand(ActiveMethodCommand):
    def execute(self):
        try:
            self.raise_NoActiveMethod()
            self.raise_InvalidName(self.name, "parameter")

            classname = self.umlclass.class_name
            methodname = self.umlmethod.name
            overload_id = self.umlmethod.overloadID

            self.driver.model.delete_parameter(classname, methodname, overload_id, self.name)
            self.set_result(CommandOutcome.SUCCESS)
        except errors.NoActiveClassException:
            return
        except errors.NoActiveMethodException:
            return
        except errors.InvalidNameException:
            return
        except errors.DuplicateMethodOverloadException as dmo_e:
            error_text = f"The resulting method signature already exists on the class {classname}."
            self.set_result(CommandOutcome.FAILED, dmo_e, error_text)
        except errors.NoSuchParameterException as nsp_e:
            error_text = f"No parameter named {self.name} in method {methodname} ({overload_id}) on class {classname} exists."
            self.set_result(CommandOutcome.FAILED, nsp_e, error_text)
        except errors.UMLException as uml_e:
            self.set_result(CommandOutcome.FAILED, uml_e)
        except Exception as e:
            self.set_result(CommandOutcome.EXCEPTION, e)

    @property
    def name(self) -> str:
        prop_index = 2
        return self._args[prop_index]

class ParameterReplaceAllCommand(ActiveMethodCommand):
    def execute(self):
        try:
            self.raise_NoActiveMethod()
            for name, ptype in self.params:
                self.raise_InvalidName(name, "parameter")
                self.raise_InvalidName(ptype, "parameter type")

            classname = self.umlclass.class_name
            methodname = self.umlmethod.name
            overload_id = self.umlmethod.overloadID
            
            self.driver.model.replace_all_parameters(classname, methodname, overload_id, self.params)
            self.set_result(CommandOutcome.SUCCESS)
        except errors.NoActiveClassException:
            return
        except errors.NoActiveMethodException:
            return
        except errors.InvalidNameException:
            return
        except errors.DuplicateMethodOverloadException as dmo_e:
            error_text = f"The resulting method signature already exists on the class {classname}."
            self.set_result(CommandOutcome.FAILED, dmo_e, error_text)
        except errors.NoSuchParameterException as nsp_e:
            error_text = f"No parameter named {self.name} in method {methodname} ({overload_id}) on class {classname} exists."
            self.set_result(CommandOutcome.FAILED, nsp_e, error_text)
        except errors.UMLException as uml_e:
            self.set_result(CommandOutcome.FAILED, uml_e)
        except Exception as e:
            self.set_result(CommandOutcome.EXCEPTION, e)

    @property
    def params(self) -> list[tuple[str, str]]:
        prop_index = 3
        return [tuple(p.split(":")) for p in self._args[prop_index:]]

class ParameterClearCommand(ActiveMethodCommand):
    """"""
    # TODO - Implement this

class RelationAddCommand(ControllerCommand):
    def execute(self):
        try:
            self.driver.model.add_relationship(self.source, self.dest, self.relation_type)
            self.set_result(CommandOutcome.SUCCESS)
        except errors.UMLException as uml_e:
            self.set_result(CommandOutcome.FAILED, uml_e)
        except Exception as e:
            self.set_result(CommandOutcome.EXCEPTION, e)
    
    @property
    def source(self) -> str:
        prop_index = 2
        return self._args[prop_index]
    
    @property
    def dest(self) -> str:
        prop_index = 3
        return self._args[prop_index]
    
    @property
    def relation_type(self) -> str:
        prop_index = 4
        return self._args[prop_index]

class RelationDeleteCommand(ControllerCommand):
    """"""
    # TODO - Implement this

class RelationSetCommand(ControllerCommand):
    """"""
    # TODO - Implement this

class QuitCommand(ControllerCommand, CallbackCommand):
    def execute(self):
        if self.driver.model.has_unsaved_changes:
            # TODO - Handle prompting for unsaved changes.
            True

UMLCOMMANDS:dict[str, UmlCommand] = {
    r"^list$": ListClassesCommand,
    r"^class list$": ListClassesCommand,
    r"^class add ([A-Za-z0-9_]*)$": AddClassCommand,
    r"^class ([A-Za-z][A-Za-z0-9_]*)$": GetUmlClassCommand,
    r"^rename ([A-Za-z0-9_]*)$": RenameClassCommand,
    r"^delete$": DeleteClassCommand,
    r"^field add ([A-Za-z0-9_]*) ([A-Za-z0-9_]*)$": AddFieldCommand,
    r"field rename ([A-Za-z0-9_]*) ([A-Za-z0-9_]*)": RenameFieldCommand,
    r"field delete ([A-Za-z0-9_]*)$": DeleteFieldCommand,
    r"^method add ([A-Za-z0-9_]*) ([A-Za-z0-9_]*)(\s([A-Za-z0-9_]*):([A-Za-z0-9_]*))*$": MethodAddCommand,
    r"^method rename ([A-Za-z0-9_]*)": MethodRenameCommand,
    r"^method delete ([A-Za-z0-9_]*)(\s([A-Za-z0-9_]*))*$": MethodDeleteCommand,
    r"^method ([A-Za-z0-9_]*)(\s([A-Za-z0-9_]*))*$": MethodContextCommand,
    r"^parameter add ([A-Za-z0-9_]*) ([A-Za-z0-9_]*)$": ParameterAddCommand,
    r"^parameter rename ([A-Za-z0-9_]*) ([A-Za-z0-9_]*)$": ParameterRenameCommand,
    r"^parameter delete ([A-Za-z0-9_]*)$": ParameterDeleteCommand,
    r"^parameter replace all(\s([A-Za-z0-9_]*):([A-Za-z0-9_]*))+$": ParameterReplaceAllCommand,
    r"^relation add ([A-Za-z0-9_]*) ([A-Za-z0-9_]*) ([A-Za-z]*)$": RelationAddCommand,
    r"^relation list$": ListRelationCommand,
    r"^quit$": QuitCommand,
    r"^controller back$": BackCommand
}