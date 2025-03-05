
from dataclasses import dataclass
from enum import Enum, auto
import argparse

from umlcontroller import UmlController
from views.umlview import UmlView
from views.umlview_cli import UmlCliView
from views.umlview_gui import UmlGuiView


class GUI_TYPE(Enum):
    CLI = auto()
    GUI = auto()

def main(gui_type:GUI_TYPE):
    """"""
    view:UmlView = None
    if gui_type == GUI_TYPE.CLI:
        view = UmlCliView()
    elif gui_type == GUI_TYPE.GUI:
        view = UmlGuiView()
    
    controller = UmlController(view)
    view.init()


    controller.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cli', nargs='?', const=GUI_TYPE.CLI)
    ns = parser.parse_args()


    gui_type:GUI_TYPE = ns.cli or GUI_TYPE.GUI

    # PROD
    # main(gui_type)

    # Dev testing only
    main(GUI_TYPE.CLI)