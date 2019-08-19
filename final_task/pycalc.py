import argparse
import importlib
import shlex
import parser_split
import operator
import RELOAD
import string

parser = argparse.ArgumentParser(description = "Parser 2.0")
parser.add_argument('cal_exp')
parser.add_argument('-math', default='math', dest='mathematics')
parser.add_argument('-m', action='append', dest='modules')
results = parser.parse_args()
parser_string = list(shlex.shlex(results.cal_exp, punctuation_chars=False))








converted_string = parser_split.split_string(parser_string)
converted_string = parser_split.conversion_signs(converted_string)
converted_strings = RELOAD.convertion_const(converted_string)
converted_strings = RELOAD.join_minus(converted_strings)
converted_strings = parser_split.merging_comparison_oper(converted_strings)
expression = parser_split.add_brackets(converted_strings)










if len(expression) == 2:   
    expression = RELOAD.solution_unar(expression)
    print(expression)
else:
    expression = RELOAD.absolute_solution(expression)
    print(expression)
    expression = RELOAD.trig_solution(expression)
    #print(expression)
    expression = RELOAD.del_brackets(expression)
    expression = RELOAD.solution_comparison(expression)
    print(expression)

    




        
                
                
                
            
        
        
        


            
             


                           




    

