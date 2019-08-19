from collections import OrderedDict
import operator
import math




OPERATORS = {'1': {'^': operator.pow},
             '2': {'/': operator.truediv, '%': operator.mod, '*': operator.mul, '//': operator.floordiv},
             '3': {'+': operator.add, '-': operator.sub}}
OPERATORS = OrderedDict(OPERATORS)

OPERATORS_TRIG = dict()

OPERATORS_CONST = dict()
                   
OPERATORS_COMPARISON = {'<': operator.lt,
                            '>': operator.gt,
                            '<=': operator.le,
                            '>=': operator.ge,
                            '!=': operator.ne,
                            '==': operator.eq
                        }
                                           
OPERATORS_UNAR = {'-': operator.neg, '+': operator.pos}                        


def fill_dict_math(module):
    """Заполнение словарей ключами и значениями"""
    for key, value in module.__dict__.items():
        if '__' in key:
            continue
        elif type(value) == float:
            OPERATORS_CONST[key] = value
        else:
            OPERATORS_TRIG[key] = value

fill_dict_math(math)

def convertion_const(expression):
    """перевод строковых констант в их численное значение"""
    for i, value in enumerate(expression):
        if value in OPERATORS_CONST:
            expression[i] = OPERATORS_CONST[value]
    return expression

                      

def absolute_solution(expr):
    """Решение с приоритетами операций"""
    for key in OPERATORS:
        i = 0
        while i < len(expr):
            if expr[i] in OPERATORS[key]:
                try:
                    type(float(expr[i-1])) and type(float(expr[i+1]))
                except:
                    i += 1
                else:
                    sing_1, sing_2 = float(expr[i-1]), float(expr[i+1])
                    expr[i-1:i+2] = [OPERATORS[key][expr[i]](sing_1,sing_2)]
                    i -= 1
            else:
                i += 1
    return expr


def trig_solution(exp):
    """Решение тригонометрических выражений и с запятой"""
    boolean = True
    while boolean:
        boolean = False
        i = 0
        while i < len(exp):
            if exp[i] in OPERATORS_TRIG and exp[i+3] == ')':
                print('da')
                if i+6 < len(exp):
                    if exp[i+6] == ')' and exp[i+4] == '(':
                        sign_1, sign_2 = float(exp[i+2]), float(exp[i+5])
                        exp[i:i+7] = [OPERATORS_TRIG[exp[i]](sign_1, sign_2)]
                        boolean = True
                        i += 1
                        print('zap')
                        print(exp)
                        continue
                sign = float(exp[i+2])
                exp[i:i+4] = [OPERATORS_TRIG[exp[i]](sign)]
                boolean = True
                print(exp)
            i += 1
        exp = absolute_solution(exp)
        print('IIocle trig')
        print(exp)
    return exp

def del_brackets(exp):
    """удаление всех скобок из строки"""
    for i, value in enumerate(exp):
        if exp[i] == '(' or exp[i] == ')':
            del exp[i]
    exp = absolute_solution(exp)
    return exp
                
def solution_comparison(exp):
    """Решение для сравнений"""
    i = 0
    while i < len(exp):
        if exp[i] in OPERATORS_COMPARISON:
            exp[i-1:i+2] = [OPERATORS_COMPARISON[exp[i]](exp[i-1],exp[i+1])]
        i += 1
    return exp

def solution_unar(exp):
    """Унарный пример"""
    if len(exp) == 2 and exp[0] in OPERATORS_UNAR:
        return OPERATORS_UNAR[exp[0]](float(exp[1]))
    return exp


def join_minus(exp):
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
                exp[i:i+2] = ["+", "-{}".format(exp[i+1])]
    
    for i, value in enumerate(exp):
        if value == '-':
            try:
                type(float(exp[i+1]))
            except ValueError:
                pass
            else:
                exp[i:i+2] = ["-{}".format(exp[i+1])]
    return exp
        
                

    
    


        
    
    


















        
            
            
