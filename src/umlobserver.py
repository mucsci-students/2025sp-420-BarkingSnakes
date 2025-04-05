from __future__ import annotations
from abc import ABC, abstractmethod

class UmlSubject(ABC):
    """Interface for implementing the Observer pattern.  The subject is the thing
    being observed."""
    @abstractmethod
    def attach(self, observer:UmlObserver):
        """Attach an observer to that wants to be notified."""
    
    @abstractmethod
    def detach(self, observer:UmlObserver):
        """Remove an observer from being notified."""
    
    @abstractmethod
    def notify(self):
        """Notify all the attached observers."""

class BaseSubject(UmlSubject):
    """Base impelmentation of UmlSubject.  You most likely do not need to override
    the implementations."""
    def __init__(self):
        self._observers:list[UmlObserver] = []

    def attach(self, observer:UmlObserver):
        """"""
        self._observers.append(observer)
    
    def detach(self, observer:UmlObserver):
        """"""
        self._observers.remove(observer)
    
    def notify(self):
        """"""
        for observer in self._observers:
            observer.update(self)

class UmlObserver(ABC):
    """The observer who defines the behavior when it is notified from the subject."""
    @abstractmethod
    def update(self, subject:UmlSubject):
        """"""