import sys
from views.umlview_observer import UmlViewObserver, UmlCommand, errors

class UmlViewCliObserver(UmlViewObserver):
    """"""
    import utilities.cli_utils as cli
    _ec = cli.get_escape_char()
    _getch = cli.getch

    DEFAULT_PROMPT = "BS-uml"
    active_class:str = None
    active_method:tuple[str, int] = None

    def get_user_input(self, tcompletes:list[str]) -> str:
        """"""
        user_input = ""
        predict = ""
        s_idx = 0
        offset_left = 0

        sys.stdout.write(self.prompt)
        sys.stdout.flush()
        while True:
            c = self._getch().decode()
            if self._char_is_special(c):
                c = self._getch().decode()
                if c == "K": # left arrow
                    """Move left"""
                    if s_idx > 0:
                        sys.stdout.write(f"{self._ec}[D")
                        offset_left += 1
                    s_idx = max(0, s_idx - 1)
            elif c == "\r": # enter (readline)
                sys.stdout.write("\r" + self.prompt + user_input + "\n")
                sys.stdout.flush()
                return user_input
            elif c == "\t": # tab
                user_input += predict
                sys.stdout.write("\r" + self.prompt + user_input)
                sys.stdout.flush()
                s_idx = len(user_input)
                offset_left = 0
            elif c == "\u0008" or c == "\x7f": # backspace
                if user_input != "":
                    user_input = user_input[:-1]
                    s_idx = len(user_input)
                sys.stdout.write(f"{self._ec}[2K\r" + self.prompt + user_input) # \033 is oct for \u001b
                sys.stdout.flush()
            elif c == "\x03": # ctrl+c
                user_input += "ctrl+c"
            elif c == "\x04": # ctrl+d
                user_input = "quit"
                return user_input
            else:
                user_input = user_input[:s_idx] + c + user_input[s_idx:]
                # s += c
                s_idx += 1
                sys.stdout.write("\r" + self.prompt + user_input)
                if offset_left > 0:
                    sys.stdout.write(f"{self._ec}[{offset_left}D")
                sys.stdout.flush()
        
            if user_input != "":
                    for tcomplete in tcompletes:
                        if tcomplete.startswith(user_input):
                            predict = tcomplete[len(user_input):]
                            sys.stdout.write(f"{self._ec}[90m" + predict + f"{self._ec}[0m" + "\u0008" * len(predict))
                            break

    def _char_is_special(self, char:str) -> bool:
        """Checks if the first keypress was a special character."""
        return char == '\000' or char == '\xe0'

    def parse_command(self, cmd_string:str) -> UmlCommand:
        """Logic to parse command strings and return an appropriate UmlCommand."""
        if cmd_string == "quit":
            return self.COMMANDS.ExitCommand(self)
        return self.COMMANDS.EchoCommand(self, cmd_string)

    def handle_umlexception(self, exception:errors.UMLException):
        """Logic to handle what to do with a UmlException."""

    @property
    def prompt(self) -> str:
        """The CLI prompt to display each loop."""
        prompt = f"{self._ec}[1;31m{self.DEFAULT_PROMPT}{self._ec}[0m"
        if self.active_class:
            prompt += f"{self._ec}[36m[{self.active_class}]{self._ec}[0m"
        if self.active_method:
            prompt += f"{self._ec}[33m[+{self.active_method[0]}({self.active_method[1]})]{self._ec}[0m"
        return rf"{prompt}{self._ec}[1;31m>{self._ec}[0m "

    def start(self):
        """Logic needed to run the UmlViewObserver."""
        import umlcommands.cli_commands
        self.COMMANDS = umlcommands.cli_commands

        tcompletes = ["quit"]
        self.running = True
        while self.running:
            cmd_string = self.get_user_input(tcompletes)
            if cmd_string:
                _command = self.parse_command(cmd_string)
                self.handle_command(_command)

    def shutdown(self):
        """Logic needed to shutdown and stop the UmlViewObserver from running."""
        self.running = False

