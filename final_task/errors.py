from calc_solution import OPERATORS_COMPARISON, OPERATORS_CONST, OPERATORS_TRIG
from string import digits, ascii_lowercase
import re
import shlex


OPERATORS = ['/', '*', '%', '^', '<', '>', '=', '!']


def foo(pars_string):
    if not pars_string:
        print(f'ERROR: empty line')
        exit(0)
    elif pars_string.count('(') != pars_string.count(')'):
        print(f'ERROR: brackets are not balanced')
        exit(0)
    elif pars_string.startswith(('=', '>', '<')):
        print(f'ERROR: no first number in the line')
        exit(0)
    elif not pars_string.endswith(((*digits), ')', (*OPERATORS_CONST.keys()))):
        print(f'ERROR: the last position is not a number or bracket')
        exit(0)
    elif ' ' in pars_string:
        i = 0
        while i < len(pars_string):
            if pars_string[i] == ' ':
                if pars_string[i-1] in list(digits) and pars_string[i+1] in list(digits):
                    print(f'ERROR: missing operator at {i} position')
                    exit(0)
                elif pars_string[i-1] in OPERATORS and pars_string[i+1] in OPERATORS:
                    print(f'ERROR: delete white space between operators')
                    exit(0)
            elif pars_string[i] in OPERATORS and pars_string[i+1] in OPERATORS[0:4]:
                print(f'ERROR: signs are not placed correctly')
                exit(0)
            i += 1
