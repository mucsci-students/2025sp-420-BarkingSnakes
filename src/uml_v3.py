from views.umlview_cli_observer import UmlViewCliObserver
from views.umlview_gui_observer import UmlViewGuiObserver, ServerThread
from gui.gui_v2 import app as gui
from umlcontroller_observer import UmlControllerObserver

def main():
    """"""
    controller = UmlControllerObserver()
    controller.model.load("test2.json")
    # cli = UmlViewCliObserver()

    # cli.attach(controller)
    # controller.attach(cli)

    # cli.start()

    # gui = setup_gui()
    gui.attach(controller)
    controller.attach(gui)
    gui_thread = ServerThread(gui)
    gui_thread.daemon = True
    gui.set_thread(gui_thread)
    gui_thread.start()

    controller.run()

if __name__ == "__main__":
    main()