# Filename: test_user_input.py
# Authors: Steven Barnes, John Hershey
# Date: 2025-02-15, Last edit date: 2025-04-18
# Description: Unit Tests CLI user input portion of UML

import pytest

from src.umlcontroller import UmlController
from src.views import umlview_cli
import src.errors as errors

app = UmlController(umlview_cli.UmlCliView())

def test_command_list_raises_exception_with_no_project_loaded():
    retval = False
    try:
        app.command_list()
    except Exception as e:
        retval = e == errors.NoActiveProjectException()
    finally:
        #project is usually always active now
        assert not retval

def test_command_class_raises_no_exception_with_no_project_loaded():
    retval = False
    try:
        app.model.add_umlclass("temp")
        app.command_class("temp")
        app.command_back()
    except Exception as e:
        retval = e == errors.NoActiveClassException()
    finally:
        assert not retval

def test_command_add_umlclass_raises_no_exception_with_no_class_context():
    retval = True
    try:
        app.command_add_umlclass("temp1")
        app.command_back()
    except Exception as e:
        assert e == None
        retval = False
    finally:
        assert retval

def test_command_delete_umlclass_raises_exception_with_no_class_context():
    retval = False
    try:
        app.command_delete_umlclass()
    except Exception as e:
        retval = e == errors.NoActiveClassException()
    finally:
        assert retval

def test_command_rename_umlclass_raises_exception_with_no_class_context():
    retval = False
    try:
        app.command_rename_umlclass("")
    except Exception as e:
        retval = e == errors.NoActiveClassException()
    finally:
        assert retval

def test_command_field_raises_exception_with_no_class_context():
    retval = False
    try:
        app.command_field()
    except Exception as e:
        retval = e == errors.NoActiveClassException()
    finally:
        assert retval

def test_command_add_field_raises_exception_with_no_class_context():
    retval = False
    try:
        app.command_add_field()
    except Exception as e:
        retval = e == errors.NoActiveClassException()
    finally:
        assert retval

def test_command_rename_field_raises_exception_with_no_class_context():
    retval = False
    try:
        app.command_rename_field()
    except Exception as e:
        retval = e == errors.NoActiveClassException()
    finally:
        assert retval

def test_command_delete_field_raises_exception_with_no_class_context():
    try:
        app.command_delete_field()
        assert False
    except Exception as e:
        assert e == errors.NoActiveClassException()