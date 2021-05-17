# Sa se gaseasca cel mai mic numar pozitiv u > 0, de forma u = 10^−m, astfel ca:
# 1.0 + u != 1.0

def get_u_min(m_increment):
    m = 0
    while 1.0 + (10 ** (-m)) != 1.0:
        m += m_increment
    m -= m_increment
    return m, 10 ** (-m)
