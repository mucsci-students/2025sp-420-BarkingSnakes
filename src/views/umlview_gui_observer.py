import threading
import re
from werkzeug.serving import make_server
from flask import Flask, request, render_template, Response, jsonify

from views.umlview_observer import UmlViewObserver
from umlcommands.base_commands import UmlCommand
import umlcommands.controller_commands as c_cmd
import errors

class ServerThread(threading.Thread):
    def __init__(self, app:Flask):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', 5001, app)
        self.ctx = app.app_context()
        self.ctx.push()
    
    def run(self):
        print("starting server")
        self.server.serve_forever()
    
    def shutdown(self):
        print("shutting down server")
        self.server.shutdown()

class UmlViewGuiObserver(Flask, UmlViewObserver):
    """"""
    def __init__(self, *args, **kwargs):
        Flask.__init__(self, *args, **kwargs)
        UmlViewObserver.__init__(self)

    def handle_umlexception(self, exception:errors.UMLException):
        """Logic to handle what to do with a UmlException."""

    def start(self):
        """Logic needed to run the UmlViewObserver."""

    def set_thread(self, thread:ServerThread):
        self._thread = thread

    def shutdown(self):
        """Logic needed to shutdown and stop the UmlViewObserver from running."""
        self._thread.shutdown()

    def parse_command(self, cmd_string:str) -> UmlCommand:
        """Logic to parse command strings and return an appropriate UmlCommand."""
        cmd_args = tuple(cmd_string.split(" "))
        for regex, cmd in c_cmd.UMLCOMMANDS.items():
            if re.search(regex, cmd_string):
                _cmd = cmd(*cmd_args)
                # if isinstance(_cmd, c_cmd.QuitCommand):
                #     exit_cmd = self.COMMANDS.ExitCommand()
                #     exit_cmd.set_driver(self)
                #     _cmd.set_callback(exit_cmd)
                # if isinstance(_cmd, c_cmd.PromptingCommand):
                #     _cmd.set_prompt_requester(self._prompt_requester)
                return _cmd