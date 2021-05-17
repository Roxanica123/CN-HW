from random import uniform

from sympy import *
import numpy as np

from read_utils import read


def get_x0():
    return uniform(-10, +10)


def get_derivative_1(f, h=10 ** -5):
    return (3 * f - 4 * f.subs(Symbol('x'), Symbol('x') - h) + f.subs(Symbol('x'), Symbol('x') - 2 * h)) / (2 * h)


def get_derivative_2(f, h=10 ** -5):
    return (- (f.subs(Symbol('x'), Symbol('x') + 2 * h)) + 8 * f.subs(Symbol('x'), Symbol('x') + h) - 8 * f.subs(
        Symbol('x'), Symbol('x') - h) + f.subs(Symbol('x'), Symbol('x') - 2 * h)) / (12 * h)


def get_second_derivative(f, h=10 ** -5):
    return (-(f.subs(Symbol('x'), Symbol('x') + 2 * h)) +
            16 * f.subs(Symbol('x'), Symbol('x') + h) -
            30 * f + 16 * f.subs(Symbol('x'), Symbol('x') - h) -
            f.subs(Symbol('x'), Symbol('x') - 2 * h)) / (12 * h ** 2)


def denominator(g, x):
    g1 = g.subs(Symbol('x'), x)
    g2 = g.subs(Symbol('x'), x + g1)
    return abs(g2 - g1)


def get_delta_x(g, x):
    g1 = g.subs(Symbol('x'), x)
    z = x + (g1 ** 2) / denominator(g, x)
    delta_x = (g1 * (g.subs(Symbol('x'), z) - g1)) / denominator(g, x)
    return delta_x


def dehghan_hajarian(g, epsilon=10 ** -15, k_max=1000):
    x = get_x0()
    k = 1
    if denominator(g, x) <= epsilon:
        return x
    delta_x = get_delta_x(g, x)
    x = x - delta_x
    while epsilon <= abs(delta_x) <= 10 ** 8 and k <= k_max:
        if denominator(g, x) <= epsilon:
            return x
        delta_x = get_delta_x(g, x)
        x = x - delta_x
        k += 1
    if abs(delta_x) < epsilon:
        return x
    return None


def check_solution(f, x, epsilon=10 ** -15):
    second_derivative = get_second_derivative(f)
    if x is None:
        print("No solution was found")
        return None
    print("Solution found: ", x)
    val = second_derivative.subs(Symbol('x'), x)
    if val > epsilon:
        print("F''(x*) = ", val, "> 0 => local/global minimum")
        return True
    else:
        print("F''(x*) = ", val, "< 0 => not a local/global minimum ")
        return False


def compare_derivatives(f, iterations=30, epsilon=10 ** -15):
    derivative_1 = get_derivative_1(f)
    derivative_2 = get_derivative_2(f)
    trues_1 = nones_1 = falses_1 = 0
    trues_2 = nones_2 = falses_2 = 0
    for i in range(iterations):
        result = check_solution(f, dehghan_hajarian(derivative_1, epsilon))
        if result is True:
            trues_1 += 1
        elif result is False:
            falses_1 += 1
        else:
            nones_1 += 1
        result = check_solution(f, dehghan_hajarian(derivative_2, epsilon))
        if result is True:
            trues_2 += 1
        elif result is False:
            falses_2 += 1
        else:
            nones_2 += 1
    print("Results:")
    print("Using first formula for the derivative:")
    print("{}/{} times the local/global minimum was found".format(trues_1, iterations))
    print("{}/{} times a solution was found but it was not a local/global minimum".format(falses_1, iterations))
    print("{}/{} times it was a fail".format(nones_1, iterations))

    print("Using second formula for the derivative:")
    print("{}/{} times the local/global minimum was found".format(trues_2, iterations))
    print("{}/{} times a solution was found but it was not a local/global minimum".format(falses_2, iterations))
    print("{}/{} times it was a fail".format(nones_2, iterations))


if __name__ == '__main__':
    function = read("2.txt")
    # derivative = get_derivative_2(function)
    # x = dehghan_hajarian(derivative, epsilon=10 ** -10)
    # check_solution(function, x)
    compare_derivatives(function, iterations=10)
