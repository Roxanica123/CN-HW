from math import sin, cos
import decimal

def read_points(path=None):
    if path is None:
        x0 = float(input("x0 = "))
        xn = float(input("xn= "))
    else:
        with open(path, "r") as f:
            x0 = float(f.readline())
            xn = float(f.readline())
    return x0, xn


def f1(x):
    return x ** 2 - 12 * x + 30


def f2(x):
    return sin(x) - cos(x)


def f3(x):
    return 2 * (x ** 3) - 3 * x + 15


def f_range(x, y, ratio):
    while x < y:
        yield float(x)
        x += decimal.Decimal(ratio)
