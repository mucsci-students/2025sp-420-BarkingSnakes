# Filename: test_user_input.py
# Authors: Steven Barnes
# Date: 2025-02-15
# Description: Unit Tests CLI user input portion of UML

import pytest

from src.umlcontroller import UmlApplication
import src.errors as errors

app = UmlApplication()

def test_command_list_raises_exception_with_no_project_loaded():
    retval = False
    try:
        app.command_list()
    except Exception as e:
        retval = e.get_num() == errors.error_list['NoActiveProjectError']
    finally:
        assert retval

def test_command_class_raises_exception_with_no_project_loaded():
    retval = False
    try:
        app.command_class()
    except Exception as e:
        retval = e.get_num() == errors.error_list['NoActiveProjectError']
    finally:
        assert retval

def test_command_add_umlclass_raises_exception_with_no_class_context():
    retval = False
    try:
        app.command_add_umlclass()
    except Exception as e:
        retval = e.get_num() == errors.error_list['NoActiveClassError']
    finally:
        assert retval

def test_command_delete_umlclass_raises_exception_with_no_class_context():
    retval = False
    try:
        app.command_delete_umlclass()
    except Exception as e:
        retval = e.get_num() == errors.error_list['NoActiveClassError']
    finally:
        assert retval

def test_command_rename_umlclass_raises_exception_with_no_class_context():
    retval = False
    try:
        app.command_rename_umlclass()
    except Exception as e:
        retval = e.get_num() == errors.error_list['NoActiveClassError']
    finally:
        assert retval

def test_command_attribute_raises_exception_with_no_class_context():
    retval = False
    try:
        app.command_attribute()
    except Exception as e:
        retval = e.get_num() == errors.error_list['NoActiveClassError']
    finally:
        assert retval

def test_command_add_attribute_raises_exception_with_no_class_context():
    retval = False
    try:
        app.command_add_attribute()
    except Exception as e:
        retval = e.get_num() == errors.error_list['NoActiveClassError']
    finally:
        assert retval

def test_command_rename_attribute_raises_exception_with_no_class_context():
    retval = False
    try:
        app.command_rename_attribute()
    except Exception as e:
        retval = e.get_num() == errors.error_list['NoActiveClassError']
    finally:
        assert retval

def test_command_delete_attribute_raises_exception_with_no_class_context():
    retval = False
    try:
        app.command_delete_attribute()
    except Exception as e:
        retval = e.get_num() == errors.error_list['NoActiveClassError']
    finally:
        assert retval