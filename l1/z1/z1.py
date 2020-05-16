import sys
import math
from random import uniform
from time import time
import numpy

k = 0.01


def happy_cat(x):
    return ((normalization(x)**2-4)**2)**(1/8) + (normalization(x)**2 / 2 + sum(x))/4 + 1/2


def normalization(x):
    return math.sqrt(sum(xi**2 for xi in x))


def griewank(x):
    return 1 + sum((xi**2)/4000 for xi in x) - numpy.prod([math.cos(xi / math.sqrt(i)) for i, xi in enumerate(x, 1)])


def new_x():
    return [uniform(-1, 1) for _ in range(4)]


def get_neighbours(x):
    return [[xi + uniform(-k, k) for xi in x] for _ in range(5)]


def tabu_search(func, max_time):
    best = new_x()
    best_candidate = best
    tabu_list = [best]
    start_time = time()

    while time() - start_time < max_time:
        s_neighborhood = get_neighbours(best_candidate)

        for s_candidate in s_neighborhood:
            if s_candidate not in tabu_list and func(s_candidate) < func(best_candidate):
                best_candidate = s_candidate

        if func(best_candidate) < func(best):
            best = best_candidate

        tabu_list.append(best_candidate)

        if len(tabu_list) > 5:
            tabu_list.remove(tabu_list[1])

    return " ".join(str(elem) for elem in best) + " " + str(func(best))


with open(sys.argv[1], 'r') as in_data:
   content = in_data.readline().split()

max_time = float(content[0])
if content[1] == 0:
    func = happy_cat
else:
    func = griewank

result = tabu_search(func, max_time)
print(result)

with open(sys.argv[2], 'w') as out_data:
  content = out_data.write(result)



