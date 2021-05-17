import random

import numpy as np

import numpy as np
import regex as re
from sklearn import datasets


def get_variables_names(lines):
    text = "".join(lines)
    return np.unique(re.findall("[a-zA-z]", text))


def get_coefficient(var, line):
    num = re.search(r"(-?[\d+]?[\.]?\d+)?" + var, line)
    if num is None:
        return 0
    return float(num.group(1)) if num.group(1) is not None else 1


def parse_equation_text(line, var_names):
    line = re.split("=", re.sub(r"\s", "", line))
    return np.array([get_coefficient(var, line[0]) for var in var_names]), np.array([float(line[1])])


def read_equations_from_console():
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    return np.array(lines)


def read_equations_from_file(file_path):
    return np.array(open(file_path).readlines())


def read_equations(file_path=None):
    lines = read_equations_from_file(file_path) if file_path is not None else read_equations_from_console()
    m = int(lines[0])
    epsilon = 10 ** -m
    lines = np.delete(lines, 0, 0)
    var_names = get_variables_names(lines)
    if var_names.size != lines.size:
        print("The system matrix is not square matrix.")
        exit(-1)
    a = np.zeros((var_names.size, var_names.size))
    b = np.zeros((var_names.size, 1))
    for i in range(var_names.size):
        a[i], b[i] = parse_equation_text(lines[i], var_names)
    return len(a), epsilon, a, b


def solve_system(file_path=None):
    n, epsilon, a, b = read_equations(file_path)
    if np.linalg.det(a) == 0:
        print("The determinant is 0, the matrix has no inverse")
        return None
    inv = np.linalg.inv(a)
    rez = inv.dot(b)
    return [str(rez[i][0]) for i in range(len(rez))]


# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------

def read_input_from_file_matrix(file_path):
    file = open(file_path)
    n, m = (int(x) for x in file.readline().split(" "))
    epsilon = 10 ** -m
    a = np.zeros((n, n))
    b = np.zeros((n, 1))
    for i in range(n):
        a[i] = [float(x) for x in file.readline().split(" ")]
    for i in range(n):
        b[i] = float(file.readline())
    return n, epsilon, a, b


def read_input_from_console_matrix():
    n, m = (int(x) for x in input().split(" "))
    epsilon = 10 ** -m
    a = np.zeros((n, n))
    b = np.zeros((n, 1))
    for i in range(n):
        a[i] = [float(x) for x in input().split(" ")]
    for i in range(n):
        b[i] = float(input())
    return n, epsilon, a, b


# print(read_input_from_file_matrix("input_matrix.txt"))
# print(read_input_from_console_matrix())
# print(solve_system("input_system.txt"))

# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------

def generate_matrix(n=100, m=10):
    a = np.random.rand(n, n).astype('float32')
    a = np.dot(a, a.transpose())
    b = np.random.randint(1, 10000, size=(n, 1)).astype('float32')
    epsilon = 10 ** -m
    for i in range(n):
        for j in range(n):
            a[i][j] = a[j][i]
    print(a)
    return n, epsilon, a, b
