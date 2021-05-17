from read_utils import read_matrix_from_file, check_symmetry
import numpy as np


def cholesky_stuff(matrix, epsilon, k_max=1000):
    l = np.linalg.cholesky(matrix)
    matrix = l.T.dot(l)
    k = 1
    while np.linalg.norm((matrix - l.dot(l.T))) > epsilon and k < k_max:
        l = np.linalg.cholesky(matrix)
        matrix = l.T.dot(l)
        k += 1
    if k < k_max:
        # matrix va fi o matrice diagonala care va contine valorile proprii
        print(k)
        return matrix
    return None


def get_p_and_q(n, a):
    max_el = -np.inf
    p_max = 0
    q_max = 0
    for i in range(n):
        for j in range(i):
            if abs(a[i][j]) > max_el:
                max_el = abs(a[i][j])
                p_max = i
                q_max = j
    return p_max, q_max


def get_c_s_and_t(a, p, q):
    alpha = (a[p][p] - a[q][q]) / (2 * a[p][q])
    alpha_sign = 1 if alpha >= 0 else -1
    t = -alpha + alpha_sign * (alpha ** 2 + 1) ** 0.5
    c = 1 / ((1 + t ** 2) ** 0.5)
    s = t / ((1 + t ** 2) ** 0.5)
    return c, s, t


def update_a(p, q, c, s, t, a, n):
    for j in range(n):
        if j != p and j != q:
            a[p][j] = c * a[p][j] + s * a[q][j]
            a[q][j] = a[j][q] = -s * a[j][p] + c * a[q][j]
            a[j][p] = a[p][j]
    a[p][p] = a[p][p] + t * a[p][q]
    a[q][q] = a[q][q] - t * a[p][q]
    a[p][q] = a[q][p] = 0
    print(p, q)
    print(a)


def update_u(p, q, c, s, u):
    for i in range(n):
        aux_uip = u[i][p]
        u[i][p] = c * u[i][p] + s * u[i][q]
        u[i][q] = -s * aux_uip + c * u[i][q]


def jacobi_method(n, a, epsilon, k_max=1000):
    k = 0
    u = np.array([[1.0 if j == i else 0.0 for j in range(n)] for i in range(n)])
    p, q = get_p_and_q(n, a)
    c, s, t = get_c_s_and_t(a, p, q) if abs(a[p][q]) > epsilon else (None, None, None)
    while abs(a[p][q]) > epsilon and k < k_max:
        update_a(p, q, c, s, t, a, n)
        update_u(p, q, c, s, u)
        p, q = get_p_and_q(n, a)
        c, s, t = get_c_s_and_t(a, p, q) if abs(a[p][q]) > epsilon else (None, None, None)
        k += 1
    if k < k_max:
        return a, u
    return (None, None)


def get_svd_info(a, p, n, epsilon):
    cv, s, vh = np.linalg.svd(a, full_matrices=True)
    print("Singular values: ", s)
    s_aux = [i for i in s if i > epsilon]
    print("Matrix rank: ", len(s_aux))
    print("Matrix rank with library: ", np.linalg.matrix_rank(a))
    max_sigma = max(s)
    min_sigma = min(s_aux)
    print("Condition number: ", max_sigma / min_sigma)
    print("Condition number with library: ", np.linalg.cond(a))
    si = np.zeros((n, p))
    for i in range(len(s_aux)):
        si[i][i] = 1 / s_aux[i]
    ai = (vh.T.dot(si)).dot(cv.T)
    print("-----------------------------------------")
    print("Moore-Penrose pseudoinverse: ")
    print(ai)
    aj = np.linalg.inv(a.T.dot(a)).dot(a.T)
    print(aj)
    print("|| Ai - Aj || =", np.linalg.norm((ai - aj), ord=1))


if __name__ == '__main__':
    p, n, epsilon, a = read_matrix_from_file("symmetric_matrix.txt")
    a_init = np.copy(a)
    if check_symmetry(a, n, p):
        values, u = jacobi_method(n, a, epsilon)
        if values is not None:
            print("||A_init*U ≈ Λ*U|| = ", np.linalg.norm((a_init.dot(u) - u.dot(values))))

    print(cholesky_stuff(np.copy(a_init), epsilon))
    print("-----------------------------------------")
    p, n, epsilon, a = read_matrix_from_file("matrix.txt")
    if p > n:
        get_svd_info(a, p, n, epsilon)
