# Proof of concept for tab complete with cmd lib
# Evan Magill , Kyle Kalbach
# 04/18/2025

import cmd

class umlShell (cmd.Cmd):
    intro = 'Welcome to Uml Shell \n'
    prompt = 'BS-UML>'
    file = None

    # Basic commands

    def do_class(self,args):
        'Changes to specified class context of the form class <classname>'
        self.prompt = args + '\n'
    
    def do_back(self,args):
        'Returns to the previous context'
        self.prompt = 'BS-UML>'

    def do_a_b (self,args):
        'Is A space B ?'
    
    def do_quit(self,args):
        'Quit the program'
        print('Exiting BS-UML')
        quit()
        return True
    
if __name__ == '__main__' :
    umlShell().cmdloop()

