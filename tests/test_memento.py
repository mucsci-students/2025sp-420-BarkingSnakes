# Filename: test_memento.py
# Authors: Steven Barnes, John Hershey, Evan Magill, Kyle Kalbach, Spencer Hoover, Juliana Vinluan
# Creation Date: 2025-04-02, Last Edit Date: 2025-04-02
# Description: Unit Tests for Memento design pattern.

from src.umlmodel import UmlProject,Caretaker,ConcreteMemento
from src.umlclass import UmlClass
from datetime import datetime

def test_save_memento():
    """Tests that a memento is returned when requested from the originator."""
    test_proj = UmlProject()
    memento = test_proj._save_memento()
    assert test_proj._validate_memento(memento)
    # assert test_proj.validate_json_schema(memento.get_state())

def test_memento_get_date():
    """Tests a concrete memento returns correct creation date."""
    before = datetime.now()
    test_proj = UmlProject()
    memento = test_proj._save_memento()
    after = datetime.now()
    memento_date = memento.get_date()

    assert before <= memento_date and memento_date <= after

def test_caretaker_backup():
    """Tests the backup method properly saves a valid memento"""
    test_proj = UmlProject()
    caretaker = Caretaker(test_proj)

    caretaker.backup()

    assert len(caretaker._mementos) == 1
    assert test_proj._validate_memento(caretaker._mementos[0])

def test_caretaker_undo_restores_correct_state():
    """Tests the caretaker can return to the previous state"""
    test_proj = UmlProject()
    caretaker = Caretaker(test_proj)

    caretaker.backup()

    test_proj.add_umlclass("testclass")

    assert len(test_proj.classes) == 1

    caretaker.undo()

    assert len(test_proj.classes) == 0
    

def test_caretaker_undo_correct_history():
    """Tests the caretaker can return to the previous state"""
    test_proj = UmlProject()
    caretaker = Caretaker(test_proj)

    caretaker.backup()

    test_proj.add_umlclass("testclass")

    caretaker.backup()

    assert len(caretaker._mementos) == 2
    assert len(caretaker._redo_stack) == 0

    caretaker.undo()

    assert len(caretaker._mementos) == 1
    assert len(caretaker._redo_stack) == 1



