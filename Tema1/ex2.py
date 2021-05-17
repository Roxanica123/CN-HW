def test_plus_associativity(a, b, c):
    left = (a + b) + c
    right = a + (b + c)
    print(left, "==", right, "?")
    return left == right


def test_multiply_associativity(a, b, c):
    left = (a * b) * c
    right = a * (b * c)
    print(left, "==", right, "?")
    return left == right
