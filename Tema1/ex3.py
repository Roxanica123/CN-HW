import math

c1 = 0.33333333333333333
c2 = 0.133333333333333333
c3 = 0.053968253968254
c4 = 0.0218694885361552


def get_x_in_interval_pi_over_2(x):
    tan_coefficient = -1 if x < 0 else 1
    x = abs(x)
    if x < math.pi / 2:
        return tan_coefficient, x
    x = x % math.pi
    if x > math.pi / 2:
        x = math.pi - x
        tan_coefficient = tan_coefficient * -1
    return tan_coefficient, x


def is_special_case(x, epsilon=10 ** -12):
    return abs(abs(x) - math.pi / 2) <= epsilon


def tan_continuous_fractions(x, p=12):
    tan_coefficient, x = get_x_in_interval_pi_over_2(x)
    epsilon = 10 ** -p
    if is_special_case(x, epsilon):
        return tan_coefficient * math.inf
    mic = 10 ** -12
    c = 1 + x / mic
    d = 1 / (1 + x * 0)
    f = (c * d) * mic
    j = 2
    aj = - x ** 2
    while abs(c * d - 1) >= epsilon:
        bj = (j - 1) * 2 + 1
        d = bj + aj * d
        d = 1 / d if d != 0 else 1 / mic
        c = bj + (aj / c)
        c = c if c != 0 else mic
        f = (c * d) * f
        j += 1
    return f * tan_coefficient


def tan_polynomials(x, x_in_pi_over_4=False):
    tan_coefficient, x = get_x_in_interval_pi_over_2(x)
    if is_special_case(x):
        return tan_coefficient * math.inf
    special = False
    if x_in_pi_over_4 and x >= math.pi / 4:
        special = True
        x = math.pi / 2 - x
    tan = x + c1 * x ** 3 + c2 * x ** 5 + c3 * x ** 7 + c4 * x ** 9
    return tan * tan_coefficient if not special else tan_coefficient * 1 / tan



