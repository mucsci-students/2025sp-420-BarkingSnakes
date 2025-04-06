import os
import webbrowser
import threading
from dataclasses import dataclass
from enum import Enum, auto
import argparse


from umlcontroller import UmlController
from views.umlview import UmlView
from views.umlview_cli import UmlCliView
from views.umlview_gui import UmlGuiView
from gui.gui import app

from views.umlview_cli_observer import UmlViewCliObserver
from umlcontroller_observer import UmlControllerObserver

class GUI_TYPE(Enum):
    CLI = auto()
    GUI = auto()

def main(gui_type:GUI_TYPE):
    """"""
    view:UmlView = None
    if gui_type == GUI_TYPE.CLI:
        # view = UmlCliView()
        # controller = UmlController(view)
        # view.init()
        # controller.run()
        view = UmlViewCliObserver()
        controller = UmlControllerObserver()

        view.attach(controller)
        controller.attach(view)

        view.start()

    elif gui_type == GUI_TYPE.GUI:

        view = UmlGuiView()
        controller = UmlController(view)
        app.set_controller(controller)
        # app.set_view(view)

        flask_thread = threading.Thread(target=app.run, kwargs={'debug':True, 'use_reloader': False})
        flask_thread.daemon = True
        flask_thread.start()

        print(webbrowser.open_new("http://127.0.0.1:5000"))
        controller.run()


        
        
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cli', nargs='?', const=GUI_TYPE.CLI)
    ns = parser.parse_args()


    gui_type:GUI_TYPE = ns.cli or GUI_TYPE.GUI

    # PROD
    main(gui_type)

    # Dev testing only
    # main(GUI_TYPE.CLI)