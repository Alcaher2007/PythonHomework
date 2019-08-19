import math

def split_string(parser_string):
    
    """Соединение целочисленных значений в float"""
    
    
    for i, value in enumerate(parser_string):
        if value=='.':
            if i==0:
                parser_string[i:i+2]=[parser_string[i]+parser_string[i+1]]
                continue
            try:
                type(int(parser_string[i-1]))
            except ValueError:
                parser_string[i:i+2]=[parser_string[i]+parser_string[i+1]]
            else:
                parser_string[i-1:i+2]=[parser_string[i-1]+parser_string[i]+parser_string[i+1]]
    return parser_string




def conversion_signs(split_string):
    
    """Замена знаков при близком расположении"""
    
    i = 0
    while i < len(split_string):
        if split_string[i] == "-" and split_string[i+1] == "-":
            split_string[i:i+2] = ["+"]
            continue
        elif split_string[i] == "+" and split_string[i+1] == "-":
            split_string[i:i+2] = ["-"]
            continue
        else:
            i += 1
    return split_string


def merging_comparison_oper(list_string):
    """Слияние операторов сравнения и выставление скобок"""
    list_oper = ['>', '<', '=', '!', '<=', '>=', '==', '!=']
    for i, value in enumerate(list_string):
        if value in list_oper and list_string[i+1] in list_oper:
            list_string[i:i+2] = [value + list_string[i+1]]
    for i, value in enumerate(list_string):
        if value in list_oper:
            list_string[i:i+1] = [')', value, '(']
            list_string.append(')')
            list_string.insert(0, '(')
            break         
    return list_string
            
def add_brackets(list_of_string):
    """Расстановка скобок перед и после запятой"""
    for i, value in enumerate(list_of_string):
        if value == ',':
            list_of_string[i:i+1] = [')', '(']
    return list_of_string
    
    
        
            
    



