# Proof of concept for tab complete with cmd lib
# Evan Magill , Kyle Kalbach
# 04/18/2025

import cmd

class umlShell (cmd.Cmd):
    intro = 'Welcome to Uml Shell \n'
    prompt = 'BS-UML> '
    file = None

    # Basic commands
    
    #def do_help(self, arg):
    #    'possibility'
    #    print('test')
    #    if arg == 'class':
    #        print('hey look')

    def help_class(self):
        print('cool')

    def help_back(self):
        print('wow')

    def do_class(self, arg):
        'Changes to specified class context of the form class <classname>'
        self.prompt = arg + ' > '
    
    def do_back(self, arg):
        'Returns to the previous context'
        self.prompt = 'BS-UML> '

    def do_a_b (self, arg):
        'Is A space B ?'
    
    def do_undocumentedCommand(self, arg):
        print('no docs')
    
    def do_quit(self, arg):
        'Quit the program'
        print('Exiting BS-UML')
        quit()
        return True
    
    def do_longCommandThatGoesLikeThis(self, arg):
        'woop'
        print('woop woop')

    def do_longCommandThatLooksThisOtherWay(self, arg):
        'zoop'
        print('zoopity',arg,'doop')

    def do_commandWithCompletes(self, arg):
        'this command has completion options'
        print('hello',arg)

    def do_EOF(self, arg):
        'closes'
        print('\nbye')
        return True

    def default(self, line):
        'no matches for your command'
        print('reached default',line)

    def completedefault(self, text, line, begidx, endidx):
        print()
        print('text', text)
        print('line', line)
        print('begidx', begidx)
        print('endidx', endidx)
        print('test', line[begidx:endidx])
        print()
        return ['list', 'of', 'options']

    def complete_commandWithCompletes(self, text, line, begidx, endidx):
        print()
        print('text', text)
        print('line', line)
        print('begidx', begidx)
        print('endidx', endidx)
        print('test', line[begidx:endidx])
        print()
        return ['world', 'worm']
    
if __name__ == '__main__' :
    umlShell().cmdloop()

