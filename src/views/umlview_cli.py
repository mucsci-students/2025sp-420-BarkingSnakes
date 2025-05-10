#Filename: umlview_cli.py
# Authors: Steven Barnes, John Hershey, Evan Magill, Kyle Kalbach, Spencer Hoover, Juliana Vinluan
# Last edit Date 2025-5-10
# Description: CLI (MVC) for UML program.
from typing import Callable

from views.umlview import *

class UmlCliView(UmlView):
    """"""
    DEFAULT_PROMPT = "BS-uml"

    def __init__(self):
        """"""
        self._active_class = None
        self._active_method = None
        self._prompt_response = None

    @property
    def prompt(self) -> str:
        """The CLI prompt to display each loop."""
        prompt = f"{self.DEFAULT_PROMPT}"
        if self.active_class:
            prompt += f"[{self.active_class}]"
        if self.active_method:
            prompt += f"[+{self.active_method[0]}({self.active_method[1]})]"
        return f"{prompt}> "

    def inform_invalid_command(self, user_response):
        print(f"Failed: {user_response} is not a valid option.")

    def prompt_user(self, prompt:str, callback:Callable) -> bool:
        """
        Prompt the user if they want to take such an action\n
        will recursively call if response was not Y/N
            Params:   
                prompt: question to ask user about their action
            Returns:
                True: if user responded "Y"
                False: if user responded "N" or invalid
        """
        _prompt = prompt + " Y/N: "
        user_response = self.get_user_input(_prompt)
        if user_response.lower() != 'y':
            if user_response.lower() != 'n':
                self.inform_invalid_command(user_response)
                #is a recursive loop until user inputs Y or N
                return self.prompt_user(prompt, callback)
            self._prompt_response = False
            return False
        return True
    
    @property
    def prompt_response(self) -> bool:
        """"""
        return self._prompt_response

    def get_user_input(self, text:str = "") -> str:
        """
        gets user input from the terminal, after prompting with uml name \
        and specified text
            Params:   
                text: the text to prompt the user after the uml name
            Returns:
                the text the user types into the terminal
        """
        user_input = input(f"{self.prompt}{text}")
        while user_input == '':
            user_input = input(f"{self.prompt}{text}")
        return user_input

    def get_user_command(self) -> list:
        """Parses user input and returns the next command to execute."""
        command = self.get_user_input()
        return command.split()

    def handle_exceptions(self, error_text:str):
        """"""
        print(error_text)

    def render_umlproject(self, project:UmlProjectData):
        """"""
        if any(project.classes):
            print(f"Displaying {len(project.classes)} classes.")
            for c in project.classes:
                self.render_umlclass(c)
        else:
            print("No classes to display.")
    
    def render_umlclass(self, umlclass:UmlClassData):
        """"""
        print(umlclass.name)
        for f in umlclass.fields:
            self.render_umlfield(f)
        
        for m in umlclass.methods:
            self.render_umlmethod(m)

    def render_umlfield(self, umlfield:UmlFieldData):
        """"""
        print(f"  -{umlfield.name} ({umlfield.type})")

    def render_umlmethod(self, umlmethod:UmlMethodData):
        """"""
        params = ", ".join([p.name for p in umlmethod.params])
        print(f"  +{umlmethod.name} ({params})")

    def render_umlmethodparam(self, umlmethodparam:UmlMethodParamData):
        """"""
        return umlmethodparam.name

    def render_umlrelationship(self, umlrelationship:UmlRelationshipData):
        """"""
        print(f"<{umlrelationship.relation_type}> {umlrelationship.source} --> {umlrelationship.destination}")

    def quit(self):
        """"""
    
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
        except errors.MethodNameNotExistsException:
            self.handle_exceptions("Failed: a method with that name and arity does not exist in this class")
        except errors.FileAlreadyExistsException:
            prompt = "Warning: A file with that name already exists.  Would you like to override the file?"
            print(self.callback)
            callback = self.callback
            self.set_callback(None)
            self.prompt_user(prompt, self.callback)
        except errors.FileHasUnsavedChangesException:
            prompt = "Warning: The current project has unsaved changes.  Do you want to continue without saving?"
            callback = self.callback
            self.prompt_user(prompt, callback)
        except errors.UMLException as uml_e:
            self.handle_exceptions(f"Operation failed:UML Error:{uml_e}")
        except EOFError:
            self.is_running = False
        except Exception as e:
            self.handle_exceptions(f"Operation failed:Error:{e}")
            # raise e
            # logging.info(f" unknown error occured: {e.args}")
