# Press the green button in the gutter to run the script.
import math
import random
import time

from ex1 import get_u_min
from ex2 import test_plus_associativity, test_multiply_associativity
from ex3 import tan_continuous_fractions, tan_polynomials


def compare_tangent_function():
    pi_over_2 = math.pi / 2
    tan_continuous_fractions_error = 0
    tan_polynomials_error = 0
    tan_continuous_fractions_time = 0
    tan_polynomials_time = 0
    tan_time = 0
    iterations = 10000
    for i in range(iterations):
        number = random.uniform(-pi_over_2, pi_over_2)
        start = time.perf_counter()
        tan_continuous_fractions_value = tan_continuous_fractions(number)
        end = time.perf_counter()

        tan_continuous_fractions_time += (end - start)
        start = time.perf_counter()
        tan_polynomials_value = tan_polynomials(number, True)
        end = time.perf_counter()

        tan_polynomials_time += (end - start)
        start = time.perf_counter()
        tan_value = math.tan(number)
        end = time.perf_counter()

        tan_time += (end - start)
        tan_continuous_fractions_error += abs(tan_continuous_fractions_value - tan_value)
        tan_polynomials_error += abs(tan_polynomials_value - tan_value)
    print("Tangent with continuous fractions")
    print("Average time: ", tan_continuous_fractions_time / iterations)
    print("Average error: ", tan_continuous_fractions_error / iterations)
    print("Tangent with polynomials")
    print("Average time: ", tan_polynomials_time / iterations)
    print("Average error: ", tan_polynomials_error / iterations)
    print("Tangent")
    print("Average time: ", tan_time / iterations)


if __name__ == '__main__':
    m, u = get_u_min(1)
    print("u minim: ", u)
    print("----------------------------\n")
    print("Plus: ", test_plus_associativity(1.0, u / 10, u / 10))
    print("----------------------------\n")
    print("Multiply: ", test_multiply_associativity(1.1, u / 10, u / 10))
    print("----------------------------\nLet's see my tangent error for pi/3")
    tan_c = tan_continuous_fractions(241)
    tan_p = tan_polynomials(241, x_in_pi_over_4=True)
    tan = math.tan(241)
    print("Tangent result", tan)
    print("Tangent with continuous fractions result: ", tan_c, " error: ", abs(tan - tan_c))
    print("Tangent with polynomials result: ", tan_p, " error: ", abs(tan - tan_p))
    print("----------------------------\n")
    compare_tangent_function()
