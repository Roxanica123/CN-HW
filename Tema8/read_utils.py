from sympy import *


def read(path=None):
    return read_from_console() if path is None else read_from_file(path)


def read_from_console():
    function = input("Give me a function: ")
    function = parse_expr(function)
    return function


def read_from_file(path):
    with open(path) as file:
        function = file.readline()
        function = parse_expr(function)
        return function
