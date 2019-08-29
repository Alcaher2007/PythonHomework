from collections import OrderedDict
import operator
import math
from typing import List, Union
from mycalc.pars_analysis import conversion_signs

"""
This module fills out dictionaries of math operators.
Also it has functions, that decide expression of parser string.
"""


OPERATORS = {'priority 1': {'^': operator.pow},
             'priority 2': {'/': operator.truediv,
                            '%': operator.mod,
                            '*': operator.mul,
                            '//': operator.floordiv},
             'priority 3': {'+': operator.add,
                            '-': operator.sub}
             }

OPERATORS = OrderedDict(OPERATORS)
OPERATORS_TRIG = dict()
OPERATORS_CONST = dict()
OPERATORS_COMPARISON = {'priority 1': {'<': operator.lt,
                                       '>': operator.gt,
                                       '<=': operator.le,
                                       '>=': operator.ge,
                                       },
                        'priority 2': {'!=': operator.ne,
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
        if key.startswith('__'):
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
            if key.startswith('__'):
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

    Args:
        number_1: this is number before operator
        number_2: this is number after operator
        i: index of list

    Example:
        '1+3' -> 1 is number_1, 3 is number_2

    Returns:
        list of str and float

    Raises:
        RuntimeError(f'Uncertainty after division by zero')
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
                    # example: 1+2/0 -> will raise a mistake.
                    if expr[i] == '/' and float(expr[i+1]) == 0:
                        raise RuntimeError(f'Uncertainty after division by zero')
                    """
                    Example: '2+5' -> 2 is number_1, 5 is number_5.
                    If number_1 and number_2 can be converted to float,
                    this example ['2', '+', '5'] turns into a number [7]
                    """
                    number_1, number_2 = float(expr[i-1]), float(expr[i+1])
                    expr[i-1:i+2] = [OPERATORS[key][expr[i]](number_1, number_2)]
                    i -= 1
            else:
                i += 1
    """
    Exam: 'log(e^e^sin(23.0),45.0)' -> ['log', '(', 'e', '^', 'e', '^', 'sin' '(', '23.0', ')', ')', '(', '45.0', ')']
    As power in Python has a associativity, after first '^' we added '(' ->
    -> ['log', '(', 'e', '(', '^', 'e', '^', 'sin' '(', '23.0', ')', ')', '(', '45.0', ')']
    This procedure is performed in 'add_brackets' function of 'pars_analysis' module.
    This means that first operation '^' will be performed after second '^' operation.
    In this example at firsh will be performed 'e^sin(23)' -> ['e', '^', 'sin' '(', '23.0', ')'].
    After that in the loop start search a '(' after '^' and if the condition is fulfilled, we delete (' after 'e'.
    Final list ['e', '^', 0.4290334443756452, ')', '(', '45.0', ')'].
    """
    for i, value in enumerate(expr):
        if value == '^' and i+3 < len(expr):
            if value == '^' and expr[i+1] == '(' and expr[i+3] != '^':
                del expr[i+1]
    return expr


def trig_solution(exp: List[Union[str, float]]) -> List[Union[str, float]]:
    """
    Solving trigonometric expressions and comma.

    Args:
        number_1: this is number before operator
        number_2: this is number after operator
        i: index of list

    Example:
        'pow(2,3)' - > ['pow', '(', '2', ')', '(', '3', ')'].
        'pow' is key of OPERATORS_TRIG of dict.
        i+6 mean that pow is operation with comma [..., '(', '3', ')'].
        The last ')' is exp[i+6].
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
                    """
                    If: expression is 'pow(2,3)' for example.
                    Else: 'sin(3)' for example, cus i+3 it's the last ')'.
                    """
                    if i+6 < len(exp):
                        """
                        Example:
                            'pow(2,3)' - > ['pow', '(', '2', ')', '(', '3', ')'].
                            'pow' is key of OPERATORS_TRIG of dict.
                            i+6 mean that pow is operation with comma [..., '(', '3', ')'].
                            The last ')' is exp[i+6].
                        """
                        if exp[i+6] == ')' and exp[i+4] == '(':
                            """
                            Example:
                                'pow(2,3,4)' -> ['pow', '(', '2', ')', '(', '3', ')', '(', '4', ')'].
                                If: in operator more than 1 comma raises error.
                                Else: expression is 'pow(2,3)' -> ['pow', '(', '2', ')', '(', '3', ')'].
                                This list converted in [8].
                            """
                            if i+9 < len(exp):
                                if exp[i+9] == ')' and exp[i+7] == '(':
                                    raise RuntimeError(f'ERROR: extra comma')
                                else:
                                    number_1, number_2 = float(exp[i+2]), float(exp[i+5])
                                    exp[i:i+7] = [OPERATORS_TRIG[exp[i]](number_1, number_2)]
                                    boolean = True
                                    i += 1
                                    continue
                            else:
                                """
                                If: round has second arg.
                                Else: just performed operation with comma.
                                """
                                if exp[i] == 'round':
                                    number_1, number_2 = float(exp[i+2]), int(exp[i+5])
                                else:
                                    number_1, number_2 = float(exp[i+2]), float(exp[i+5])
                                exp[i:i+7] = [OPERATORS_TRIG[exp[i]](number_1, number_2)]
                                boolean = True
                                i += 1
                                continue
                    # This construction raises an exception for acos, asin, atan and etc.
                    number = float(exp[i+2])
                    try:
                        [OPERATORS_TRIG[exp[i]](number)]
                    except ValueError:
                        raise RuntimeError(f'ERROR: {exp[i]} function has range of -1 to 1')
                    else:
                        exp[i:i+4] = [OPERATORS_TRIG[exp[i]](number)]
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
            exp = [False]
        else:
            exp = [True]
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
        if value == '-' and exp[i+1] in OPERATORS_TRIG and (i == 0 or exp[i-1] == '('):
            exp[i:i+1] = ['-1', '*']
    return exp


fill_dict_math(math)
