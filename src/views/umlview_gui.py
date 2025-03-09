from dataclasses import dataclass
from flask import Response, jsonify

from views.umlview import *
from renderable import Renderable
from gui.renderables import UmlClassListRenderable
import errors

@dataclass
class UmlGuiView(UmlView):
    """"""
    command:str = ""
    renderable:Renderable = None
    _active_class:str = None
    _umlexception:errors.UMLException = None

    def render(self, renderable:Renderable):
        self.renderable = renderable

    def get_user_command(self) -> list[str]:
        """"""
        print("[View]Waiting for a command from flask.")
        while self.command == "":
            True
        print("Got command: ", self.command)
        return self.command.split()
        

    def set_command(self, command:str):
        """"""
        self.command = command

    def get_renderable(self) -> Renderable:
        """"""
        return self.renderable
    
    def set_active_class(self, name:str):
        """"""
        self._active_class = name

    @property
    def active_class(self) -> str:
        """"""
        return self._active_class
    
    @property
    def get_umlexception(self) -> errors.UMLException:
        """"""
        return self._umlexception

    def set_umlexception(self, e:errors.UMLException):
        """"""
        self._umlexception = e

    def handle_exceptions(self, error_text:str):
        """"""
        response = {
            "error": error_text
        }
        self.response = jsonify(response), 400

    def handle_umlexception(self, uml_exception:errors.UMLException):
        """"""
        try:
            raise uml_exception
        except errors.NoActiveProjectException:
                self.handle_exceptions("Failed: No project has been loaded.")
        except errors.NoActiveClassException:
            self.handle_exceptions("Failed: No active class selection.")
        except errors.DuplicateClassException:
            self.handle_exceptions("Failed: A class with that name already exists in this project.")
        except errors.DuplicateFieldException:
            self.handle_exceptions("Failed: A field with that name already exists on this class.")
        except errors.InvalidFileException:
            self.handle_exceptions("Failed: File must be in .json format.")
        except errors.DuplicateRelationshipException:
            self.handle_exceptions("Failed: This relationship already exists in this project.")
        except errors.NoSuchObjectException as nso_e:
            self.handle_exceptions(f"Failed: That {nso_e.object_type} does not exist.")
        except errors.InvalidNameException:
            self.handle_exceptions("Failed: That name contains invalid characters, or begins with a number.")
        except errors.MethodOverloadNotExistsException:
            self.handle_exceptions("Failed: The arity level does not exist for this method.")
        except errors.NoActiveMethodException:
            self.handle_exceptions("Failed: Not in a method context. Use: method help")
        except errors.DuplicateMethodOverloadException:
            self.handle_exceptions("Failed: An arity level already exists for the target method.")
        except errors.UMLException as uml_e:
            self.handle_exceptions(f"Operation failed:UML Error:{uml_e}")
        except EOFError:
            self.is_running = False
        except Exception as e:
            self.handle_exceptions(f"Operation failed:Error:{e}")
            # raise e
            # logging.info(f" unknown error occured: {e.args}")
    
    def get_umlproject(self) -> UmlProjectData:
        """"""
        self.project_dto = None
        self.set_active_class(None)
        self.set_command("list")
        while self.project_dto is None:
            True
        return self.project_dto

    def get_umlclass(self, name:str = None) -> UmlClassData:
        self.class_dto = None
        if name:
            self.set_active_class(None)
            self.set_command(f"class {name}")
            while self.active_class is None:
                True
        if self.active_class:
            self.set_command("list")
            while self.class_dto is None:
                True
            return self.class_dto
        

    def render_umlproject(self, project:UmlProjectData):
        """"""
        self.project_dto = project
    
    def render_umlclass(self, umlclass:UmlClassData):
        """"""
        self.class_dto = umlclass

    def render_umlfield(self, umlfield:UmlFieldData):
        """"""

    def render_umlmethod(self, umlmethod:UmlMethodData):
        """"""

    def render_umlmethodparam(self, umlmethodparam:UmlMethodParamData):
        """"""

    def render_umlrelationship(self, umlrelationship:UmlRelationshipData):
        """"""
        self.relation_dto = umlrelationship