from typing import List


def join_float(parser_list: List[str]) -> List[str]:
    """
    Joining integer values ​​in float
    """
    for i, value in enumerate(parser_list):
        if value == '.':
            if i == 0:
                parser_list[i:i+2] = [parser_list[i]+parser_list[i+1]]
                continue
            try:
                type(int(parser_list[i-1]))
            except ValueError:
                parser_list[i:i+2] = [parser_list[i]+parser_list[i+1]]
            else:
                parser_list[i-1:i+2] = [parser_list[i-1]+parser_list[i]+parser_list[i+1]]
    return parser_list


def conversion_signs(split_string: List[str]) -> List[str]:
    """
    Close character replacement
    """
    i = 0
    while i < len(split_string):
        if split_string[i] == "-" and split_string[i+1] == "-":
            split_string[i:i+2] = ["+"]
            continue
        elif split_string[i] == "+" and split_string[i+1] == "-":
            split_string[i:i+2] = ["-"]
            continue
        elif split_string[i] == "-" and split_string[i+1] == "+":
            split_string[i:i+2] = ["-"]
            continue
        elif split_string[i] == "+" and split_string[i+1] == "+":
            split_string[i:i+2] = ["+"]
            continue
        else:
            i += 1
    return split_string


def merging_comparison_oper(list_string):
    """
    Merging comparison operators and brackets
    """
    list_oper = ['>', '<', '=', '!', '<=', '>=', '==', '!=']
    for i, value in enumerate(list_string):
        if value in list_oper and list_string[i+1] in list_oper:
            list_string[i:i+2] = [value + list_string[i+1]]
    return list_string


def add_brackets(list_of_string):
    """Brackets before and after the comma"""
    for i, value in enumerate(list_of_string):
        if value == ',':
            list_of_string[i:i+1] = [')', '(']
        elif value == '^' and i+2 < len(list_of_string):
            if value == '^' and list_of_string[i+2] == '^':
                list_of_string[i:i+1] = [value, '(']
    return list_of_string
