from copy import deepcopy
from math import cos, pi, sqrt
from random import gauss
from time import time
from random import random
from math import exp


def salomon(xs):
    sqrt_sum = sqrt(sum(x ** 2 for x in xs))
    return 1 - cos(2 * pi * sqrt_sum) + 0.1 * sqrt_sum


def temp(xs):
    return [x * gauss(1, 0.1) for x in xs]


def cooler(t):
    return t * 0.99


def annealing(solution, temperature, timeout):
    temperature = temperature
    current_solution = solution
    best_solution = current_solution
    best_result = salomon(current_solution)

    start = time()
    while time() - start <= timeout:
        temp_solution = temp(deepcopy(current_solution))
        current_result = salomon(current_solution)
        temp_result = salomon(temp_solution)

        if temp_result <= current_result or (random() < exp((current_result - temp_result) / temperature)):
            current_solution = temp_solution
            current_result = temp_result

        if current_result <= best_result:
            best_solution = current_solution
            best_result = current_result

        temperature = cooler(temperature)

    return best_solution, best_result


def main():
    t, x1, x2, x3, x4 = map(float, input().split())

    best_solution, best_result = annealing(
        solution=(x1, x2, x3, x4),
        temperature=10 ** 10,
        timeout=t,
    )

    print(*best_solution, best_result)


if __name__ == "__main__":
    main()
