from typing import List, Union


def cast_to_float(parser_list: List[str]) -> List[str]:
    """
    Joining integer values ​​in float
    """
    i = 0
    while i < len(parser_list):
        if parser_list[i] == '.':
            if i == 0:
                parser_list[i:i+2] = [parser_list[i] + parser_list[i+1]]
                i += 1
                continue
            elif not parser_list[i-1].isdigit() and parser_list[i+1].isdigit():
                if parser_list[i-1].count('.') >= 1:
                    raise RuntimeError(f'ERROR: In the number there is an extra point')
                parser_list[i:i+2] = [parser_list[i] + parser_list[i+1]]
                i += 1
                continue
            elif parser_list[i-1].isdigit() and parser_list[i+1].isdigit():
                parser_list[i-1:i+2] = [parser_list[i-1] + parser_list[i] + parser_list[i+1]]
                i -= 1
                continue
        elif parser_list[i] == '/' and parser_list[i+1] == '/':
            parser_list[i:i+2] = ['//']
            i += 1
            continue
        else:
            i += 1
    return parser_list


def conversion_signs(split_list: List[str]) -> List[str]:
    """
    Folding signs
    """
    i = 0
    while i < len(split_list):
        if split_list[i] == "-" and split_list[i+1] == "-":
            split_list[i:i+2] = ["+"]
            continue
        elif split_list[i] == "+" and split_list[i+1] == "-":
            split_list[i:i+2] = ["-"]
            continue
        elif split_list[i] == "-" and split_list[i+1] == "+":
            split_list[i:i+2] = ["-"]
            continue
        elif split_list[i] == "+" and split_list[i+1] == "+":
            split_list[i:i+2] = ["+"]
            continue
        else:
            i += 1
    return split_list


def merging_comparison_oper(split_list: List[Union[str, float]]) -> List[Union[str, float]]:
    """
    Merging comparison operators
    """
    list_oper = ['>', '<', '=', '!', '<=', '>=', '==', '!=']
    for i, value in enumerate(split_list):
        if value in list_oper and split_list[i+1] in list_oper:
            split_list[i:i+2] = [value + split_list[i+1]]
    return split_list


def add_brackets(list_of_string: List[Union[str, float]]) -> List[Union[str, float]]:
    """
    replacing a comma with an opening and closing bracket
    and also adding '(' after '^'.
    """
    for i, value in enumerate(list_of_string):
        if value == ',':
            list_of_string[i:i+1] = [')', '(']
        elif value == '^' and i+2 < len(list_of_string):
            if value == '^' and list_of_string[i+2] == '^':
                list_of_string[i:i+1] = [value, '(']
    return list_of_string
