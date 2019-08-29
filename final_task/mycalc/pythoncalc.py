import argparse
import shlex
from mycalc.pars_analysis import cast_to_float, conversion_signs, merging_comparison_oper, add_brackets
from mycalc.calc_solution import *
import importlib.util
import mycalc.errors
from typing import List, Union


"""
This module is main. It makes assignments of functions from other modules,
line parsing and the final result calculation.
"""


def cmd_parser() -> str:
    parser = argparse.ArgumentParser(description="Pure-python command-line calculator.",
                                     usage='%(prog)s [-h] EXPRESSION [-m MODULE [MODULE ...]]')
    parser.add_argument('cal_exp', metavar='EXPRESSION', type=str, help='expression string to evaluate')
    parser.add_argument('-m', '--use-modules', metavar='MODULE', nargs='*',
                        dest='modules', help="additional modules to use")
    results = parser.parse_args()
    return results.cal_exp, results.modules


def check_module(module_name: list) -> str:
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


def calc(exp: str, module: list = None) -> Union[str, bool, float, int]:
    """
    It's function, which collects all functions together and does the counting
    """
    parser_list = list(shlex.shlex(exp, punctuation_chars=False))
    if module:
        modules_spec = check_module(module)
        modules_launch = import_module_from_spec(modules_spec)
        if modules_launch:
            fill_dict_user_modules(modules_launch)

    mycalc.errors.print_errors(exp)

    exp_list = conversion_signs(cast_to_float(parser_list))
    exp_with_convert_const = convertion_const(exp_list)
    exp_with_join_minus = join_minus(exp_with_convert_const)
    exp_with_merging_comparison = merging_comparison_oper(exp_with_join_minus)
    exp_with_add_brackets = add_brackets(exp_with_merging_comparison)
    converted_expression = replace_minus_trig(exp_with_add_brackets)

    decision_unar_operations = solution_unar(converted_expression)
    decision_math_opers = absolute_solution(decision_unar_operations)
    decision_trig_opers = trig_solution(decision_math_opers)
    exp_after_del_brackets = del_brackets(decision_trig_opers)
    final_result = solution_comparison(exp_after_del_brackets)
    return final_result[0]


def main_call() -> None:
    exp, module = cmd_parser()
    try:
        result = calc(exp, module)
    except Exception as error:
        print(f'{error}')
    else:
        print(result)


if __name__ == '__main__':
    main_call()
