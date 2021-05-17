class TridiagonalMatrix:
    def __init__(self, file):
        self.a, self.b, self.c, self.p, self.q = self.read_matrix(file)

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
        for i in range(n - q):
            b.append(float(file.readline()))
        file.readline()
        for i in range(n - p):
            c.append(float(file.readline()))
        return a, b, c, p, q
