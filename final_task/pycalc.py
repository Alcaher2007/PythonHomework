import argparse
import shlex
import pars_analysis
import calc_solution
import importlib.util
from typing import List


"""
This module is main. It makes assignments of functions from other modules,
line parsing and the final result calculation.
"""


parser = argparse.ArgumentParser(description = "Pure-python command-line calculator.", prefix_chars='+')
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


def calculator() -> float or bool:
    """
    It's function, which collects all functions together and does the counting
    """
    if results.modules:
        modules = check_module(results.modules)
        modules_launch = import_module_from_spec(modules)
        if modules_launch:
            calc_solution.fill_dict_user_modules(modules_launch)
    converted_string = pars_analysis.join_float(parser_string)
    converted_string = pars_analysis.conversion_signs(converted_string)
    converted_strings = calc_solution.convertion_const(converted_string)
    converted_strings = calc_solution.join_minus(converted_strings)
    converted_strings = pars_analysis.merging_comparison_oper(converted_strings)
    expression = pars_analysis.add_brackets(converted_strings)
    expression = calc_solution.replace_minus_trig(expression)

    
    def solut_func(expression: List[str or float]) -> List[float or bool]:
        """
        this function changes list of parse and does counting
        """
        if len(expression) == 2:   
            expression = calc_solution.solution_unar(expression)
            return expression
        else:
            expression = calc_solution.absolute_solution(expression)
            expression = calc_solution.trig_solution(expression)
            expression = calc_solution.del_brackets(expression)
            expression = calc_solution.solution_comparison(expression)
            return expression
    expression = solut_func(expression)
    return expression[0]


#print(calculator())










        
                
                
                
            
        
        
        


            
             


                           




    

