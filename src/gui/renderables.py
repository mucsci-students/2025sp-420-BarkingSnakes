from flask import render_template

from renderable import Renderable
from umlmodel import UmlProject
from umlclass import UmlClass

class UmlClassListRenderable(Renderable):

    def __init__(self, classes:list[UmlClass]):
        self.classes = [c.to_dict() for c in classes]

    def render(self):
        return render_template('classlist.html', classes=self.classes)
    
class UmlClassRenderable(Renderable):

    def __init__(self, umlclass:UmlClass):
        self.umlclass = umlclass.to_dict()

    def render(self):
        return render_template('activeclass.html', umlclass=self.umlclass)

