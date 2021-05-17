def read_polynomial(path=None):
    if path is None:
        return read_from_console()
    else:
        return read_from_file(path)


def read_from_console():
    polynomial = input("Polynomial coefficients: ")
    return [float(coefficient) for coefficient in polynomial.split(", ")]


def read_from_file(path):
    polynomial = open(path).read().split(", ")
    return [float(coefficient) for coefficient in polynomial]
