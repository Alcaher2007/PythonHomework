import argparse
import shlex
from pars_analysis import join_float, conversion_signs, merging_comparison_oper, add_brackets
from calc_solution import *
import importlib.util
import errors
from typing import List, Union


"""
This module is main. It makes assignments of functions from other modules,
line parsing and the final result calculation.
"""


parser = argparse.ArgumentParser(description="Pure-python command-line calculator.", prefix_chars='+')
parser.add_argument('cal_exp')
parser.add_argument('+m', '++use-modules', metavar='MODULE', nargs='*',
                    dest='modules', help="additional modules to use")
results = parser.parse_args()
parser_string = list(shlex.shlex(results.cal_exp, punctuation_chars=False))


def check_module(module_name):
    """
    Checks whether it is possible to import modules without actually importing them.
    """
    modules = list()
    for i, value in enumerate(module_name):
        if importlib.util.find_spec(value) is None:
            print('Module: {} not found'.format(value))
        else:
            print('Module: {} can be imported!'.format(value))
            modules.append(importlib.util.find_spec(value))
    return modules


def import_module_from_spec(module_spec):
    """
    The function  accepts 'import_module_from_spec'
    the module specification returned by the function check_module.
    The function module_from_spec returns import module and function
    exec_module launches it.
    """
    module = list()
    for i, value in enumerate(module_spec):
        module.append(importlib.util.module_from_spec(value))
        value.loader.exec_module(module[i])
    return module


def calc() -> Union[str, bool, float, int]:
    """
    It's function, which collects all functions together and does the counting
    """
    if results.modules:
        modules = check_module(results.modules)
        modules_launch = import_module_from_spec(modules)
        if modules_launch:
            fill_dict_user_modules(modules_launch)
    errors.foo(results.cal_exp)
    expression = replace_minus_trig(add_brackets(merging_comparison_oper(join_minus(
        convertion_const(conversion_signs(join_float(parser_string)))))))

    def solut_func(expression: List[Union[str, float]]) -> List[Union[str, bool, int, float]]:
        """
        this function changes list of parse and does counting
        """
        if len(expression) == 2:
            expression = solution_unar(expression)
            return expression
        else:
            expression = solution_comparison(del_brackets(trig_solution(absolute_solution(expression))))
            return expression

    result = solut_func(expression)
    print(result[0])


if __name__ == '__main__':
    calc()
