import numpy as np


class TridiagonalMatrixSystem:
    def __init__(self, matrix_file, f_file, p=15, k_max=1000, max_delta=10 ** 8):
        self.a, self.b, self.c, self.p, self.q = self.read_matrix(matrix_file)
        self.epsilon = 10 ** -p
        self.verify_diagonal()
        self.f = self.read_f(f_file)
        self.k_max = k_max
        self.max_delta = max_delta
        self.x = None

    @staticmethod
    def read_matrix(file):
        file = open(file)
        n = int(file.readline())
        p = int(file.readline())
        q = int(file.readline())
        a = []
        b = []
        c = []
        file.readline()
        for i in range(n):
            a.append(float(file.readline()))
        file.readline()
        for i in range(n - p):
            c.append(float(file.readline()))
        file.readline()
        for i in range(n - q):
            b.append(float(file.readline()))
        return a, b, c, p, q

    @staticmethod
    def read_f(file):
        file = open(file)
        n = int(file.readline())
        file.readline()
        f = []
        for i in range(n):
            f.append(float(file.readline()))
        return f

    def verify_diagonal(self):
        for i in self.a:
            if i <= self.epsilon:
                raise Exception("An element of the main diagonal is 0!")

    def gauss_seidel(self):
        xgs = [0 for i in self.f]
        delta = self.update_x(xgs)
        k = 1
        while self.epsilon <= delta <= self.max_delta and k <= self.k_max:
            delta = self.update_x(xgs)
            k += 1
        if self.epsilon > delta:
            self.x = xgs
            return xgs
        return None

    def update_x(self, x):
        delta = 0
        for i in range(len(x)):
            xi = (self.f[i] - (self.c[i - self.p] * x[i - self.p] if i - self.p > 0 else 0) - (
                self.b[i] * x[i + self.q] if i + self.q < len(x) else 0)) / self.a[i]
            delta += (x[i] - xi) * (x[i] - xi)
            x[i] = xi
        return delta

    def matrix_dot_solution(self):
        result = [0 for i in range(len(self.x))]
        for i in range(len(self.x)):
            result[i] = self.a[i] * self.x[i] + (self.c[i - self.p] * self.x[i - self.p] if i - self.p > 0 else 0) + (
                self.b[i] * self.x[i + self.q] if i + self.q < len(self.x) else 0)
        return result

    def verify_solution(self):
        try:
            return np.linalg.norm(np.array(self.matrix_dot_solution()) - np.array(self.f), ord=np.inf)
        except:
            return "No solution found"
