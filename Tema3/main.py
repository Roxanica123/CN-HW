from rare_matrix import RareMatrix
from tridiagonal_matrix import TridiagonalMatrix

if __name__ == '__main__':
    b = TridiagonalMatrix("b.txt")
    a = RareMatrix("a.txt")
    a_plus_b_computed = a.plus_tridiagonal_matrix(b)
    a_plus_b = RareMatrix("a+b.txt")
    print(a_plus_b_computed.is_equal(a_plus_b))
    a_dot_b_computed = a.dot_tridiagonal_matrix(b)
    a_dot_b = RareMatrix("axb.txt")
    print(a_dot_b_computed.is_equal(a_dot_b))
