

from views.umlview import *

class UmlCliView(UmlView):
    """"""
    DEFAULT_PROMPT = "BS-uml"

    def __init__(self):
        """"""
        self._active_class = None
        self._active_method = None

    @property
    def prompt(self) -> str:
        """The CLI prompt to display each loop."""
        prompt = f"{self.DEFAULT_PROMPT}"
        if self.active_class:
            prompt += f"[{self.active_class}]"
        if self.active_method:
            prompt += f"[+{self.active_method[0]}({self.active_method[1]})]"
        return f"{prompt}> "

    def prompt_user(self, prompt:str) -> bool:
        """
        Prompt the user if they want to take such an action\n
        will recursively call if response was not Y/N
            Params:   
                prompt: question to ask user about their action
            Returns:
                True: if user responded "Y"
                False: if user responded "N" or invalid
        """
        user_response = self.get_user_input(prompt)
        if user_response.lower() != 'y':
            if user_response.lower() != 'n':
                self.inform_invalid_command(user_response)
                #is a recursive loop until user inputs Y or N
                return self.prompt_user(prompt)
            return False
        return True
    
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
        print(f"  -{umlfield.name}")

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
