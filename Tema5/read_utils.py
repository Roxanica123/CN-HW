import numpy as np


def read_matrix_from_file(file_path):
    file = open(file_path)
    p, n, m = (int(x) for x in file.readline().split(" "))
    epsilon = 10 ** -m
    a = np.zeros((p, n))
    for i in range(p):
        a[i] = [float(x) for x in file.readline().split(" ")]
    return p, n, epsilon, a


def read_matrix_from_console():
    p, n, m = (int(x) for x in input().split(" "))
    epsilon = 10 ** -m
    a = np.zeros((p, n))
    for i in range(p):
        a[i] = [float(x) for x in input().split(" ")]
    return p, n, epsilon, a


def check_symmetry(matrix, n, p):
    if n != p:
        return False
    for i in range(len(matrix)):
        for j in range(i):
            if matrix[i][j] != matrix[j][i]:
                print("The matrix is not symmetric!")
                return False
    return True


def get_matrix_array_bonus(a, n):
    v = []
    for i in range(n):
        for j in range(i + 1):
            v.append(a[i][j])
    return np.array(v)
