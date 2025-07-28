"""
Contains utility functions for the main Python script
"""

from pywintypes import com_error # pyright: ignore[reportMissingModuleSource]
from win32com.client.dynamic import CDispatch 

#############################################################################################
# Color Constants
#############################################################################################

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



#############################################################################################
# Classes
#############################################################################################

class EmailNotFoundException(NameError):
    """
    Raised to indicate that an email address was not found in the user's account.

    Inherits from NameError.
    """
    pass



#############################################################################################
# Functions
#############################################################################################

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


# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------


def remove_variants(text: str) -> str:
    """
    Returns a lowercased copy of `text`, without diacritics, Leetspeak, and spaces.

    Example: if a letter in the input text is 'ä', '@', or '4', it will be replaced by the non-variant letter 'a'.

    Parameters:
        text: the text to remove variants from
    Returns:
        str: standardized version of the input text
    """
    assert isinstance(text, str), "input must be a string"

    outChars=["àáâãäå4@", "ç", "ð", "èéëêœæ3", "ìíîï1!", "òóôõöø0", "ǹńñň", "5ß", "ùúûü", "ýÿ", "⁰₀", "¹₁", "²₂", "³₃", "⁴₄", "⁵₅", "⁶₆", "⁷₇", "⁸₈", "⁹₉"]
    inChars=['a', 'c', 'd', 'e', 'i', 'o', 'n', 's', 'u', 'y', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    assert len(outChars) == len(inChars), "INTERNAL ERROR- outChars and inChars must be the same length"

    charMappingDict = dict()

    #Load the mapping dictionary: all outChars mapped to corresponding inChar
    for i, inChar in enumerate(inChars):
        for outChar in outChars[i]:
            charMappingDict[outChar] = inChar
    

    output=""

    #loop through each character of the text
    for textChar in text:

        #check if the character can be replaced: if so, replace it and append to the output
        if textChar.lower() in charMappingDict:
            output += charMappingDict.get(textChar, '')
        
        #check alphanumeric: if so, add
        elif textChar.isalnum():
            output += textChar.lower()

    return output


# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------


def send_outlook_email(outlook_instance: CDispatch, sender: str, recipient: str, subject: str, body: str) -> None:
    """
    Uses the Outlook instance `outlook_instance` to send an email from `sender` to `recipient`, 
    with the subject `subject` and the message content `body`.

    If `sender` is not an email address in the user's account, raises EmailNotFoundException (a subclass of NameError).  
    If `recipient` is not a valid email address, raises EmailNotFoundException.

    Parameters:
        outlook_instance (win32com.client.dynamic.CDispatch): Windows API Outlook instance to use
        sender (str): email address to send from
        recipient (str): email address to receive the sent message
        subject (str): subject line of the message
        body (str): contents of the message
    """
    assert isinstance(outlook_instance, CDispatch), "outlook instance must be of type win32com.client.dynamic.CDispatch"
    assert isinstance(sender, str), "sender must be a string"
    assert isinstance(recipient, str), "recipient must be a string"
    assert isinstance(subject, str), "subject must be a string"
    assert isinstance(body, str), "body must be a string"

    #Create email address and load it with parameters
    mail = outlook_instance.CreateItem(0)
    mail.Subject = subject
    mail.To = recipient
    mail.Body = body

    #Check all of the user's accounts for the sender's email
    From = None
    for myEmailAddress in outlook_instance.Session.Accounts:
        if sender in str(myEmailAddress):
            From = myEmailAddress
            break
        
    #Send the email if the given email address exists
    if From != None:
        # This line basically calls the "mail.SendUsingAccount = xyz@email.com" outlook VBA command
        mail._oleobj_.Invoke(*(64209, 0, 8, 0, From))

        # enclose email sending in try/except to stop nasty errors
        try:
            mail.Send()
        except com_error: #from pywintypes: error for bad email send
            raise EmailNotFoundException(f'The receiving email "{recipient}" was not found')

    else:
        raise EmailNotFoundException(f'The sending email "{sender}" was not found')
    