"""
Module for printing in color using ANSI escape sequences in a readable way.

The module contains constants that represent ANSI escape sequences.

The module also contains methods for printing in color, avoiding statements like:
`print(f"{RED}Hello world{DEFAULT}")`
"""


DEFAULT = '\033[39m'
"""ANSI escape sequence for printing in the console's default color"""

RED = '\033[31m'
"""ANSI escape sequence for printing in red"""

YELLOW = '\033[33m'
"""ANSI escape sequence for printing in yellow"""

GREEN = '\033[32m'
"""ANSI escape sequence for printing in green"""

BLUE = '\033[34m'
"""ANSI escape sequence for printing in blue"""

PURPLE = '\033[35m'
"""ANSI escape sequence for printing in purple"""


def printc(escape_sequence: str, contents: str = "", end: str = '\n', flush: bool = False) -> None:
    """
    "Print in Color": Prints `contents` to the standard output in color. 
    The print color is specified by the ANSI escape sequence `escape_sequence`.

     If `escape_sequence` is not a valid ANSI escape sequence, the invalid escape sequence will be printed
     before `contents`. `contents` will not change color.

     After `contents` are printed, the print color switches to the console's default color.

    Parameters:
        escape_sequence (str): color escape sequence to use
        contents (str, default=""): contents to print to the standard output
        end (str, default="\\n"): string to print after `contents`, mimicking Python's print statement
        flush (bool, default=False): whether to flush the print stream
    """
    assert isinstance(escape_sequence, str), "escape sequence must be a string"
    assert isinstance(contents, str), "contents must be a string"
    assert isinstance(end, str), "end parameter must be a string"
    assert isinstance(flush, bool), "flush parameter must be a boolean"

    print(f"{escape_sequence}{contents}{DEFAULT}", end=end, file=None, flush=flush)
