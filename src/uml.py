# Filename: uml.py
# Authors: Steven Barnes
# Date: 2025-02-02
# Description: Entry point for UML editor program.

from __future__ import annotations

import os
import json
import sys
import re

from .umlclass import UmlClass, Attribute

class UmlProject:
    """"""
    def __init__(self):
        self.classes:dict[str,UmlClass] = {}
        self._data:dict = {}

    def load(self, filepath:str) -> int:
        """"""
        if self._validate_filepath(filepath):
            return -1
        
        with open(filepath, "r") as f:
            self._data =  json.load(f)

        return 0
    
    def parse_uml_data(self) -> int:
        """"""
        uml_classes:list[dict] = self._data.get("classes")

        if uml_classes is None:
            return -1
        
        self.classes = {c.class_name:c for c in map(self._parse_uml_class, uml_classes)}

    def _parse_uml_class(self, data:dict) -> UmlClass:
        """"""
        def _parse_uml_attributes(data:dict) -> Attribute:
            """"""
            if data:
                attribute = Attribute()
                attribute.name = data.get("name")
                return attribute

            return None
        
        uml_attributes:list[Attribute] = []
        if data.get("attributes"):
            uml_attributes.extend(list(map(_parse_uml_attributes, data.get("attributes"))))
        return UmlClass(
            data.get("class_name"),
            {attribute.name:attribute for attribute in uml_attributes}
        )


    def save(self, filepath:str) -> int:
        """"""
    
    def _validate_filepath(self, filepath:str) -> int:
        """"""
        if not os.path.exists(filepath):
            return -1
        
        if not os.path.isfile(filepath):
            return -1

        if not re.search('\.json', filepath, flags=re.IGNORECASE):
            return -1

        return 0

class UmlApplication:
    """"""
    def __init__(self):
        """"""
        COMMANDS = {
            'INITIALIZE': self.setup_program,
            'NEW-PROJECT': self.new_project
        }
        self._current_filepath = None
        self.project:UmlProject = None
        self._command = COMMANDS.get('INITIALIZE')
        self._retval = 0
        self.command_stack = [self._command]
        self.is_running = True
        

    def setup_program(self):
        """Validates requirements for the program are met before attempting to start."""
        if self.project is None:
            self.get_filepath_from_user()
            self.project = UmlProject()
            self.project.load(self._current_filepath)
    
    def load_project(self) -> None:
        """"""
        self.get_filepath_from_user()
        self.project = UmlProject()
        self._retval = self.project.load(self._current_filepath)

    def new_project(self) -> None:
        """"""

    def inform_invalid_command(self, command:str) -> None:
        print(f"Invalid command: {command}.  Use command 'help' for a list of valid commands.")

    def get_filepath_from_user(self) -> None:
        self._current_filepath = input("Filepath: ")
    
    def get_user_command(self) -> None:
        command = input("uml> ")
        self._command = self.COMMANDS.get(command.upper())
        if self._command is None:
            self.inform_invalid_command(command)

    def run(self):
        """"""
        while self.is_running:
            if self._command is None:
                self.get_user_command()
            self._command()


def main():
    """Entry point for the program."""
    project = UmlProject()

if __name__ == "__main__":
    main()