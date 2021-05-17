from tridiagonal_matrix_system import TridiagonalMatrixSystem

system1 = TridiagonalMatrixSystem("a1.txt", "f1.txt")
print(system1.gauss_seidel())
print(system1.verify_solution())

system2 = TridiagonalMatrixSystem("a2.txt", "f2.txt")
system2.gauss_seidel()
print(system2.verify_solution())

system3 = TridiagonalMatrixSystem("a3.txt", "f3.txt", k_max=100000, max_delta=10**20)
system3.gauss_seidel()
print(system3.verify_solution())


system4 = TridiagonalMatrixSystem("a4.txt", "f4.txt")
system4.gauss_seidel()
print(system4.verify_solution())


system5 = TridiagonalMatrixSystem("a5.txt", "f5.txt", k_max=100000, max_delta=10**20)
system5.gauss_seidel()
print(system5.verify_solution())
