from base_commands import CliCommand, Callback


class ExitCommand(CliCommand):
    def execute(self):
        self.cli.running = False
