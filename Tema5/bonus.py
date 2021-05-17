import numpy as np

from read_utils import read_matrix_from_file, check_symmetry, get_matrix_array_bonus


def get_index(p, q):
    return p * (p + 1) // 2 + q


def get_p_and_q(a, n):
    max_el = -np.inf
    p_max = 0
    q_max = 0
    for i in range(n):
        for j in range(i):
            if abs(a[get_index(i, j)]) > max_el:
                max_el = abs(a[get_index(i, j)])
                p_max = i
                q_max = j
    return p_max, q_max


def get_c_s_and_t(a, p, q):
    alpha = (a[get_index(p, p)] - a[get_index(q, q)]) / (2 * a[get_index(p, q)])
    alpha_sign = 1 if alpha >= 0 else -1
    t = -alpha + alpha_sign * (alpha ** 2 + 1) ** 0.5
    c = 1 / ((1 + t ** 2) ** 0.5)
    s = t / ((1 + t ** 2) ** 0.5)
    return c, s, t


def update_a(p, q, c, s, t, a, n):
    for j in range(p):
        if j != q:
            aux = a[get_index(p, j)]
            a[get_index(p, j)] = c * a[get_index(p, j)] + s * a[get_index(q, j)]
            if j < q:
                a[get_index(q, j)] = -s * aux + c * a[get_index(q, j)]
            else:
                a[get_index(j, q)] = -s * aux + c * a[get_index(j, q)]
    for j in range(p + 1, n):
        aux = a[get_index(j, p)]
        a[get_index(j, p)] = c * a[get_index(j, p)] + s * a[get_index(j, q)]
        a[get_index(j, q)] = -s * aux + c * a[get_index(j, q)]
    a[get_index(p, p)] = a[get_index(p, p)] + t * a[get_index(p, q)]
    a[get_index(q, q)] = a[get_index(q, q)] - t * a[get_index(p, q)]
    a[get_index(p, q)] = 0
    print(p, q)
    print(a)


def update_u(p, q, c, s, u):
    for i in range(n):
        aux_uip = u[i][p]
        u[i][p] = c * u[i][p] + s * u[i][q]
        u[i][q] = -s * aux_uip + c * u[i][q]


def jacobi_method_bonus(n, a, epsilon, k_max=10000):
    k = 0
    u = np.array([[1.0 if j == i else 0.0 for j in range(n)] for i in range(n)])
    p, q = get_p_and_q(a, n)
    c, s, t = get_c_s_and_t(a, p, q) if abs(a[get_index(p, q)]) > epsilon else (None, None, None)
    while abs(a[get_index(p, q)]) > epsilon and k < k_max:
        update_a(p, q, c, s, t, a, n)
        update_u(p, q, c, s, u)
        p, q = get_p_and_q(a, n)
        c, s, t = get_c_s_and_t(a, p, q) if abs(a[get_index(p, q)]) > epsilon else (None, None, None)
        k += 1
    if k < k_max:
        return a, u
    return None, None


if __name__ == '__main__':
    p, n, epsilon, a = read_matrix_from_file("symmetric_matrix.txt")
    if check_symmetry(a, n, p):
        v = get_matrix_array_bonus(a, n)
        print(v)
        values, u = jacobi_method_bonus(n, v, epsilon)
        print(values)
        print(u)
