from collections import OrderedDict
import operator
import math
from typing import List, Union
from mycalc.pars_analysis import conversion_signs

"""
This module fills out dictionaries of math operators.
Also it has functions, that decide expression of parser string.
"""


OPERATORS = {'1': {'^': operator.pow},
             '2': {'/': operator.truediv,
                   '%': operator.mod,
                   '*': operator.mul,
                   '//': operator.floordiv},
             '3': {'+': operator.add,
                   '-': operator.sub}
             }

OPERATORS = OrderedDict(OPERATORS)
OPERATORS_TRIG = dict()
OPERATORS_CONST = dict()
OPERATORS_COMPARISON = {'1': {'<': operator.lt,
                              '>': operator.gt,
                              '<=': operator.le,
                              '>=': operator.ge,
                              },
                        '2': {'!=': operator.ne,
                              '==': operator.eq
                              }
                        }
OPERATORS_COMPARISON = OrderedDict(OPERATORS_COMPARISON)
OPERATORS_UNAR = {'-': operator.neg, '+': operator.pos}


def fill_dict_math(module: str) -> None:
    """
    Filling out dictionaries with keys and values from the math library.
    """
    for key, value in module.__dict__.items():
        if '__' in key:
            continue
        elif type(value) == float:
            OPERATORS_CONST[key] = value
        else:
            OPERATORS_TRIG[key] = value
    OPERATORS_TRIG['abs'] = abs
    OPERATORS_TRIG['round'] = round


def fill_dict_user_modules(list_of_modules: list) -> None:
    """
    Filling dictionaries with keys and values ​​from imported modules.
    """
    for i, value in enumerate(list_of_modules):
        for key, values in value.__dict__.items():
            if '__' in key:
                continue
            elif type(values) == float:
                OPERATORS_CONST[key] = values
            else:
                OPERATORS_TRIG[key] = values


def convertion_const(expression: List[str]) -> List[Union[str, float]]:
    """
    replacement of string constants with their numerical value.
    """
    for i, value in enumerate(expression):
        if value in OPERATORS_CONST:
            expression[i] = OPERATORS_CONST[value]
    return expression


def absolute_solution(expr: List[Union[str, float]]) -> List[Union[str, float]]:
    """
    Operational Priority Solution and delete sign '(' after 'e'.
    """
    for key in OPERATORS:
        i = 0
        while i < len(expr):
            if expr[i] in OPERATORS[key]:
                try:
                    type(float(expr[i-1])) and type(float(expr[i+1]))
                except ValueError:
                    i += 1
                else:
                    if expr[i] == '/' and float(expr[i+1]) == 0:
                        raise RuntimeError(f'Uncertainty after division by zero')
                    sing_1, sing_2 = float(expr[i-1]), float(expr[i+1])
                    expr[i-1:i+2] = [OPERATORS[key][expr[i]](sing_1, sing_2)]
                    i -= 1
            else:
                i += 1
    for i, value in enumerate(expr):
        if value == '^' and i+3 < len(expr):
            if value == '^' and expr[i+1] == '(' and expr[i+3] != '^':
                del expr[i+1]
    return expr


def trig_solution(exp: List[Union[str, float]]) -> List[Union[str, float]]:
    """
    Solving trigonometric expressions and comma.
    """
    boolean = True
    while boolean:
        boolean = False
        i = 0
        while i < len(exp):
            if type(exp[i]) == str:
                if exp[i][0].isalpha() and exp[i] not in OPERATORS_TRIG:
                    raise RuntimeError(f'ERROR: unknown function {exp[i]}')
                elif exp[i] in OPERATORS_TRIG and exp[i+3] == ')':
                    if i+6 < len(exp):
                        if exp[i+6] == ')' and exp[i+4] == '(':
                            if i+9 < len(exp):
                                if exp[i+9] == ')' and exp[i+7] == '(':
                                    raise RuntimeError(f'ERROR: extra comma')
                                else:
                                    sign_1, sign_2 = float(exp[i+2]), float(exp[i+5])
                                    exp[i:i+7] = [OPERATORS_TRIG[exp[i]](sign_1, sign_2)]
                                    boolean = True
                                    i += 1
                                    continue
                            else:
                                if exp[i] == 'round':
                                    sign_1, sign_2 = float(exp[i+2]), int(exp[i+5])
                                else:
                                    sign_1, sign_2 = float(exp[i+2]), float(exp[i+5])
                                exp[i:i+7] = [OPERATORS_TRIG[exp[i]](sign_1, sign_2)]
                                boolean = True
                                i += 1
                                continue
                    sign = float(exp[i+2])
                    try:
                        [OPERATORS_TRIG[exp[i]](sign)]
                    except ValueError:
                        raise RuntimeError(f'ERROR: {exp[i]} function has range of -1 to 1')
                    else:
                        exp[i:i+4] = [OPERATORS_TRIG[exp[i]](sign)]
                        boolean = True
            i += 1
        exp = absolute_solution(exp)
    return exp


def del_brackets(exp: List[Union[str, float]]) -> List[Union[str, float]]:
    """
    remove all brackets from a string.
    """
    i = 0
    while i < len(exp):
        if exp[i] == '(' or exp[i] == ')':
            del exp[i]
            continue
        i += 1
    exp = absolute_solution(solution_unar(conversion_signs(exp)))
    try:
        float(exp[0])
    except TypeError:
        pass
    else:
        exp[0] = float(exp[0])
    return exp


def solution_comparison(exp: List[Union[str, float]]) -> List[Union[str, float, bool]]:
    """
    Solving for operators of comparison.
    """
    comparison_list = list()
    for key in OPERATORS_COMPARISON:
        i = 0
        while i < len(exp):
            if exp[i] in OPERATORS_COMPARISON[key]:
                comparison_list.append(OPERATORS_COMPARISON[key][exp[i]](float(exp[i-1]), float(exp[i+1])))
            i += 1
    if comparison_list:
        if False in comparison_list:
            exp[:] = [False]
        else:
            exp[:] = [True]
    return exp


def solution_unar(exp: List[Union[str, float]]) -> List[Union[str, float]]:
    """
    Unary operations solution.
    """
    if exp[0] in OPERATORS_UNAR:
        try:
            type(float(exp[1]))
        except ValueError:
            pass
        else:
            exp[0:2] = [OPERATORS_UNAR[exp[0]](float(exp[1]))]
    exp = absolute_solution(exp)
    return exp


def join_minus(exp: List[Union[str, float]]) -> List[Union[str, float]]:
    """
    Add minuses to the numbers on the right and also near consts.
    Adding a plus, where necessary.
    """
    for i, value in enumerate(exp):
        if value == '-':
            try:
                type(float(exp[i-1])) and type(float(exp[i+1]))
            except ValueError:
                try:
                    type(float(exp[i+1]))
                except ValueError:
                    pass
                else:
                    if exp[i-1] == ')':
                        exp[i:i+2] = ["+", "-{}".format(exp[i+1])]
            else:
                if i+2 < len(exp):
                    if exp[i+2] == '^':
                        continue
                exp[i:i+2] = ["+", "-{}".format(exp[i+1])]

    for i, value in enumerate(exp):
        if value == '-':
            try:
                type(float(exp[i+1]))
            except ValueError:
                pass
            else:
                if i+2 < len(exp):
                    if exp[i+2] == '^':
                        continue
                exp[i:i+2] = ["-{}".format(exp[i+1])]
    return exp


def replace_minus_trig(exp: List[Union[str, float]]) -> List[Union[str, float]]:
    """
    Replacing the minus near trigonometrical expression with '-1 *'
    """
    for i, value in enumerate(exp):
        if value == '-' and exp[i+1] in OPERATORS_TRIG and (exp[i-1] == '(' or i == 0):
            exp[i:i+1] = ['-1', '*']
    return exp


fill_dict_math(math)
