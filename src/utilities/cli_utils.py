import os
import sys
import psutil
import subprocess
from typing import Callable

getch:Callable[[], bytes] = None
getche:Callable[[], bytes] = None

if os.name == "nt":
    # FOR WINDOWS SYSTEMS
    import msvcrt
    getch = msvcrt.getch
    getche = msvcrt.getche
elif os.name == "posix":
    # FOR UNIX SYSTEMS
    import tty
    import termios
    # See https://stackoverflow.com/questions/1052107/reading-a-single-character-getch-style-in-python-is-not-working-in-unix
    class _GetchUnix:
        def __init__(self):
            import tty, sys

        def __call__(self):
            import sys, tty, termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch.encode()


    getch = _GetchUnix()

def get_escape_char() -> str:
    """Sets the escape character sequence dependant on the terminal that
    that launched the program.  
    PowerShell versions >=6 uses the sequence '`e'.  
    PowerShell versions <6 uses the sequence '$([char]27)'.  
    Unix shells use the sequence '\\u001b'."""

    ec = "\u001b"

    term_prog = os.environ.get('TERM_PROGRAM')
    if term_prog and term_prog == 'vscode':
        return ec

    proc = psutil.Process(os.getpid())
    while proc:
        if proc.name() == "powershell.exe":
            # print("Setting escape character for PowerShell.")
            result = subprocess.run(["powershell.exe", "$PSVersionTable.PSVersion.Major"], stdout=subprocess.PIPE)
            psversion = int(result.stdout.decode().strip())
            if psversion >= 6:
                ec = "`e"
            else:
                ec = "$([char]27)"
            break
        proc = proc.parent()

    return ec

    