import sys
from . dictionary import *


def interpret(match, inputstr):

    inputstr = inputstr.strip()
    if(len(inputstr) == 0):
        return True

    tokens = inputstr.split(" ", 1)
    if(len(tokens) == 2):
        params = tokens[1]
    else:
        params = ""

    for dword in dictionary:
        if(dword.name == tokens[0]):
            return dword.code(match, params)

    print("???")
    return True


def forth():
    lstparam = ['White', 'm', 'Black', "h"]
    match = new_match(lstparam)

    if(init_words() == False):
        return

    while(True):
        calc_and_domove(match)

        inputstr = input("OK ")

        if(interpret(match, inputstr) == False):
            break

