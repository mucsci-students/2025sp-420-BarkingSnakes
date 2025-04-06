from views.umlview_cli_observer import UmlViewCliObserver

def main():
    """"""
    cli = UmlViewCliObserver()
    cli.attach(cli)
    cli.start()

if __name__ == "__main__":
    main()