from copy import deepcopy

from tridiagonal_matrix import TridiagonalMatrix


class RareMatrix:
    def __init__(self, file=None, matrix=None, epsilon=10 ** -10):
        if file is not None:
            self.matrix = self.read_matrix(file)
        else:
            self.matrix = matrix
        self.epsilon = epsilon

    @staticmethod
    def read_matrix(file):
        file = open(file)
        n = int(file.readline())
        matrix = [{} for i in range(n)]
        file.readline()
        line = file.readline()
        while line:
            line = line.split(", ")
            val = float(line[0])
            i = int(line[1])
            j = int(line[2])
            if j in matrix[i]:
                matrix[i][j] += val
            else:
                matrix[i][j] = val
            line = file.readline()
        return matrix

    def plus_tridiagonal_matrix(self, b: TridiagonalMatrix):
        if len(self.matrix) != len(b.a):
            return None
        matrix = deepcopy(self.matrix)
        for i in range(len(b.a)):
            if i in matrix[i]:
                matrix[i][i] += b.a[i]
            else:
                matrix[i][i] = b.a[i]

        for i in range(len(b.a) - b.q):
            if i + b.q in matrix[i]:
                matrix[i][i + b.q] += b.b[i]
            else:
                matrix[i][i + b.q] = b.b[i]

        for i in range(b.p, len(b.a)):
            if i - b.p in matrix[i]:
                matrix[i][i - b.p] += b.c[i - b.p]
            else:
                matrix[i][i - b.p] = b.c[i - b.p]
        return RareMatrix(matrix=matrix)

    def dot_tridiagonal_matrix(self, b: TridiagonalMatrix):
        if len(self.matrix) != len(b.a):
            return None
        matrix = [{} for i in range(len(b.a))]
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                sum = 0
                if j >= b.q and j - b.q in self.matrix[i]:
                    sum += self.matrix[i][j - b.q] * b.b[j - b.q]
                if j < len(b.a) - b.p and j + b.p in self.matrix[i]:
                    sum += self.matrix[i][j + b.p] * b.c[j]
                if j in self.matrix[i]:
                    sum += self.matrix[i][j] * b.a[j]
                if abs(sum) >= self.epsilon:
                    matrix[i][j] = sum
        return RareMatrix(matrix=matrix)

    def is_equal(self, matrix):
        if len(self.matrix) != len(matrix.matrix):
            return False
        for i in range(len(self.matrix)):
            if self.matrix[i].keys() != matrix.matrix[i].keys():
                return False
            for key in self.matrix[i].keys():
                if abs(self.matrix[i][key] - matrix.matrix[i][key]) >= self.epsilon:
                    return False
        return True
