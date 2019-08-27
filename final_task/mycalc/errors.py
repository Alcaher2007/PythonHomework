from mycalc.calc_solution import OPERATORS_COMPARISON, OPERATORS_CONST, OPERATORS_TRIG
from string import digits, ascii_lowercase
import re
import shlex

"""
error search module
"""

OPERATORS = ['/', '*', '%', '^', '<', '>', '=', '!']


def print_errors(pars_string: str) -> None:
    """
    Search errors and raising exceptions.
    """
    if not pars_string:
        raise RuntimeError(f'ERROR: empty line')
    elif pars_string.count('(') != pars_string.count(')'):
        raise RuntimeError(f'ERROR: brackets are not balanced')
    elif pars_string.startswith(('=', '>', '<')):
        raise RuntimeError(f'ERROR: no first number in the line')
    elif not pars_string.endswith(((*digits), ')', (*OPERATORS_CONST.keys()))):
        raise RuntimeError(f'ERROR: the last position is not a number or bracket')
    elif ' ' in pars_string:
        i = 0
        while i < len(pars_string):
            if pars_string[i] == ' ':
                if pars_string[i-1] in list(digits) and pars_string[i+1] in list(digits):
                    raise RuntimeError(f'ERROR: missing operator at {i} position')
                elif pars_string[i-1] in OPERATORS and pars_string[i+1] in OPERATORS:
                    raise RuntimeError(f'ERROR: delete white space between operators')
            elif pars_string[i] in OPERATORS and pars_string[i+1] in OPERATORS[0:4]:
                raise RuntimeError(f'ERROR: signs are not placed correctly')
            i += 1
