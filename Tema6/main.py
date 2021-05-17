from utils import read_points, f1, f2, f3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def generate_points(x0, xn, function, n):
    points = np.linspace(x0, xn, num=n + 1)
    points = list(map(lambda x: (x, function(x)), points))
    return points


def generate_system(points, m):
    a = []
    b = []
    for i in range(m + 1):
        coefficients = []
        for j in range(m + 1):
            sum = 0
            for k in range(len(points)):
                sum += points[k][0] ** (i + j)
            coefficients.append(sum)
        a.append(coefficients)
        sum = 0
        for k in range(len(points)):
            sum += points[k][1] * points[k][0] ** i
        b.append(sum)
    return a, b


def horner(solution, x, epsilon=10 ** -15):
    solution = [x for x in solution]
    d = solution[0]
    for i in range(1, len(solution)):
        d = solution[i] + d * x
    return d


def least_squares_method(points, m=4):
    a, b = generate_system(points, m)
    solution = np.linalg.solve(a, b)
    return solution[::-1], points


def spline_functions(points, da, x):
    ai = da
    for i in range(len(points) - 1):
        h = points[i + 1][0] - points[i][0]
        aii = -ai + 2 * (points[i + 1][1] - points[i][1]) / h
        if points[i][0] <= x <= points[i + 1][0]:
            return ((aii - ai) / (2 * h)) * ((x - points[i][0]) ** 2) + ai * (x - points[i][0]) + points[i][1]
        ai = aii


def plot_points(points, d, solution, f, n=1000):
    x_values = np.linspace(x0, xn, num=n + 1)
    df = pd.DataFrame(
        {'x_values': x_values, 'y1_values': [f(x) for x in x_values],
         'y2_values': [horner(solution, x) for x in x_values],
         'y3_values': [spline_functions(points, d, x) for x in x_values]
         })
    plt.plot('x_values', 'y1_values', data=df, marker='', color='skyblue', linewidth=4, label="Original function")
    plt.plot('x_values', 'y2_values', data=df, marker='', color='olive', linewidth=2, label="Least squares method")
    plt.plot('x_values', 'y3_values', data=df, marker='', color='green', linewidth=1, label="Spline functions")
    plt.legend()
    plt.show()
    plt.clf()


if __name__ == '__main__':
    x0, xn = read_points("in.txt")
    points = generate_points(x0, xn, f1, 10)
    solution, points = least_squares_method(points)
    print("---------------Least squares method______________")
    print("System solution:", solution)
    x = 2.5
    print("|Pm(x) - f(x)| = ", abs(horner(solution, x) - f1(x)))
    sum = 0
    for i in range(len(points)):
        sum += abs(horner(solution, points[i][0]) - points[i][1])
    print("sum(|Pm(xi) - yi|) = ", sum)
    d = -10
    print("---------------Spline functions______________")
    print("Sf(x) = ", spline_functions(points, d, x))
    print("|Sf(x) - f(x)| = ", abs(spline_functions(points, d, x) - f1(x)))
    plot_points(points, d, solution, f1)

    x0, xn = 0, 1.5
    points = generate_points(x0, xn, f2, 10)
    solution, points = least_squares_method(points)
    plot_points(points, 1, solution, f2, 10)

    x0, xn = 0, 2
    points = generate_points(x0, xn, f3, 10)
    solution, points = least_squares_method(points)
    plot_points(points, -3, solution, f3, 5)

