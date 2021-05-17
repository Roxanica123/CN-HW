import sys

from scipy.linalg import cho_factor, cho_solve
import numpy as np
import math

from read_utils import read_input_from_file_matrix, generate_matrix, read_input_from_console_matrix
import argparse


def check_symmetry_and_positive_definite(matrix, epsilon):
    for i in range(len(matrix)):
        if matrix[i][i] < 0 and abs(matrix) <= epsilon:
            print("The matrix is not positive definite!")
            exit(-1)
        for j in range(i):
            if matrix[i][j] != matrix[j][i]:
                print("The matrix is not symmetric!")
                exit(-1)


def get_cholesky_decomposition(a_matrix, epsilon):
    d = [a_matrix[i][i] for i in range(len(a_matrix))]

    for p in range(len(a_matrix)):
        lpp_sum = d[p]
        for j in range(p):
            lpp_sum -= a_matrix[p][j] ** 2
        if abs(lpp_sum) <= epsilon:
            print("The matrix is not positive definite!")
            exit(-1)
        a_matrix[p][p] = math.sqrt(lpp_sum)

        for i in range(p + 1, len(a_matrix)):
            lip_sum = a_matrix[i][p]
            for j in range(p):
                lip_sum -= a_matrix[i][j] * a_matrix[p][j]
            a_matrix[i][p] = lip_sum / a_matrix[p][p]
    return a_matrix, d


def get_determinant(l_p):
    determinant = 1
    for i in range(len(l_p)):
        determinant *= l_p[i][i]
    return determinant * determinant


def direct_substitution(a_matrix, b_vector, epsilon):
    x = np.zeros((len(b_vector), 1))
    for i in range(len(b_vector)):
        x_sum = b_vector[i].copy()
        for j in range(i):
            x_sum -= a_matrix[i][j] * x[j]
        if abs(a_matrix[i][i]) <= epsilon:
            print("Can't divide to 0")
            exit(-1)
        x[i] = x_sum / a_matrix[i][i]
    return x


def inverse_substitution(a_matrix, b_vector, epsilon):
    x = np.zeros((len(b_vector), 1))
    for i in reversed(range(len(b_vector))):
        x_sum = b_vector[i].copy()
        for j in range(i + 1, len(b_vector)):
            x_sum -= a_matrix[i][j] * x[j]
        if abs(a_matrix[i][i]) <= epsilon:
            print("Can't divide to 0")
            exit(-1)
        x[i] = x_sum / a_matrix[i][i]
    return x


def verify_solution(a, d, x, b):
    y = np.zeros((len(b), 1))
    for i in range(len(a)):
        for j in range(len(a)):
            y[i] += a[j][i] * x[j] if j < i else d[i] * x[j] if i == j else a[i][j] * x[j]
    sum = 0
    for i in range(len(y)):
        sum += (y[i] - b[i]) ** 2
    return str(sum)


def solve_system_with_numpy(a, b, epsilon):
    l = np.linalg.cholesky(a)
    y = direct_substitution(l, b, epsilon)
    x = inverse_substitution(l.transpose(), y, epsilon)
    return l, x


def solve_system_with_scipy(a, b):
    c, low = cho_factor(a)
    x = cho_solve((c, low), b)
    return x


def get_cholesky_inverse(l):
    a_inverse = np.zeros((len(l), len(l)))
    for i in range(len(l)):
        b = np.array([1.0 if j == i else 0.0 for j in range(len(l))]).transpose()
        y = direct_substitution(l, b, epsilon)
        x = inverse_substitution(l.transpose(), y, epsilon).reshape((len(l),))
        a_inverse[:, i] = x
    return a_inverse


def verify_inverse(np_inverse, inverse):
    return "||Cholesky_inverse- Numpy inverse||:\n" + str(np.linalg.norm(np_inverse - inverse))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_file', '-if',
                        default=None, help="File path")
    parser.add_argument('--rand', '-r',
                        default=True, help="The number of concurrent requests")
    parser.add_argument('--in_console', '-ic', default=False)
    parser.add_argument('--out_file', '-of',
                        default=None, help="File path")
    parser.add_argument('--n', '-n', default=10)
    args = parser.parse_args(sys.argv[1:])
    if args.in_file is not None:
        n, epsilon, a, b = read_input_from_file_matrix(args.in_file)
    elif args.in_console is True:
        n, epsilon, a, b = read_input_from_console_matrix()
    else:
        n, epsilon, a, b = generate_matrix(int(args.n))

    result = ""
    numpy_inverse = np.linalg.inv(a)
    check_symmetry_and_positive_definite(a, epsilon)
    l_numpy, x_numpy = solve_system_with_numpy(a, b, epsilon)
    x_scipy = solve_system_with_scipy(a, b)
    a, d = get_cholesky_decomposition(a, epsilon)

    result += "L in matrix A:\n" + str(a) + "\n"
    det = get_determinant(a)
    result += "Determinant:\n" + str(det) + "\n"
    y = direct_substitution(a, b, epsilon)
    x = inverse_substitution(a.transpose(), y, epsilon)
    result += "||A_init*x - b||: \n"
    result += verify_solution(a, d, x, b)
    result += "\nCholesky solution: \n" + str(x) + "\n"
    result += "Numpy matrix and solution:\n" + str(l_numpy) + "\n"
    result += str(x_numpy) + "\n"
    result += verify_inverse(numpy_inverse, get_cholesky_inverse(a))
    if args.out_file is None:
        print(result)
    else:
        open(args.out_file, 'w').write(result)
