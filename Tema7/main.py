import math
from random import random, uniform

import numpy

from utils import read_polynomial


def horner(coefficients, x, epsilon=10 ** -15):
    d = coefficients[0]
    for i in range(1, len(coefficients)):
        d = coefficients[i] + d * x
    return d


def get_x0(coefficients):
    r = abs(coefficients[0]) + max([abs(a) for a in coefficients]) / abs(coefficients[0])
    return uniform(-r, +r)


def get_delta_x(coefficients, x, epsilon=10 ** -9):
    sub = (int(horner(get_derivative_coefficients(coefficients), x)) ** 3)
    sub = sub if sub > epsilon else epsilon
    ck = ((int(horner(coefficients, x)) ** 2) * horner(
        get_derivative_coefficients(get_derivative_coefficients(coefficients)), x)) / sub
    delta_xk = horner(coefficients, x) / horner(get_derivative_coefficients(coefficients), x) + ck / 2
    return delta_xk


def olivers_method(coefficients, epsilon=10 ** -9, k_max=1000000):
    x = get_x0(coefficients)
    k = 0
    delta_x = 0
    if abs(horner(get_derivative_coefficients(coefficients), x)) >= epsilon:
        delta_x = get_delta_x(coefficients, x, epsilon)
        x = x - delta_x
        k += 1
        while epsilon <= abs(delta_x) <= 10 ** 8 and k <= k_max:
            if abs(horner(get_derivative_coefficients(coefficients), x)) <= epsilon:
                break
            delta_x = get_delta_x(coefficients, x)
            x = x - delta_x
            k += 1
    if abs(delta_x) < epsilon:
        return x
    else:
        return None


def get_roots(coefficients, n_iterations=1000, precision=10 ** -9):
    roots_set = set()
    for i in range(n_iterations):
        x = olivers_method(coefficients=polynomial_coefficients)
        if x is not None:
            roots_set.add(x)
    distinct_roots = []
    roots_set = list(roots_set)
    for i in range(len(roots_set)):
        distinct = True
        for j in range(i):
            if abs(roots_set[i] - roots_set[j]) < precision:
                distinct = False
        if distinct is True:
            distinct_roots.append(roots_set[i])
    return distinct_roots


def get_derivative_coefficients(coefficients):
    reversed_coefficients = coefficients[::-1]
    derivative_coefficients = []
    for i in range(1, len(reversed_coefficients)):
        derivative_coefficients.append(i * reversed_coefficients[i])
    return derivative_coefficients[::-1]


def write_roots(roots, path):
    with open(path, "w") as file:
        for root in roots:
            file.write(str(root) + "\n")


if __name__ == '__main__':
    polynomial_coefficients = read_polynomial("in.txt")
    roots = get_roots(coefficients=polynomial_coefficients, n_iterations=100)
    print(roots)
    write_roots(roots, "out.txt")
