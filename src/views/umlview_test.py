#file for testing commands that can prompt the user
from views.umlview import *

class UmlTestView(UmlView):
    """Class for test view when autnatically doing pytest of input-related commands
    """

    def __init__(self):
        """"""
        self._active_class = None
        self._active_method = None
        self._prompt_response = None
        self._prompt_text = None
        

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
        error_return = f"Failed: {user_response} is not a valid option."
        raise errors.TestViewPromptException(error_return)

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
        raise errors.TestViewPromptException(text)

    def get_user_command(self) -> list:
        """Parses user input and returns the next command to execute."""
        command = self.get_user_input()
        return command.split()

    def handle_exceptions(self, error_text:str):
        """"""
        raise errors.TestViewPromptException(error_text)

    def set_active_class(self, name:str):
        """"""
        self._active_class = name

    @property
    def active_class(self) -> str:
        """"""
        return self._active_class

    def set_active_method(self, method:tuple[str, int]):
        """"""
        self._active_method = method

    @property
    def active_method(self) -> tuple[str, int]:
        """"""
        return self._active_method

    def render_umlproject(self, project:UmlProjectData):
        """print nothing when using pytest"""
        return
    
    def render_umlclass(self, umlclass:UmlClassData):
        """print nothing when using pytest"""
        return

    def render_umlfield(self, umlfield:UmlFieldData):
        """print nothing when using pytest"""
        return

    def render_umlmethod(self, umlmethod:UmlMethodData):
        """print nothing when using pytest"""
        return

    def render_umlmethodparam(self, umlmethodparam:UmlMethodParamData):
        """"""
        return umlmethodparam.name

    def render_umlrelationship(self, umlrelationship:UmlRelationshipData):
        """print nothing when using pytest"""
        return

    def quit(self):
        """"""
    
    def handle_umlexception(self, uml_exception:errors.UMLException):
        """raise error for test class to notice"""
        raise uml_exception