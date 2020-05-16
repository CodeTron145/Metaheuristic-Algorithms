from math import exp
from sys import maxsize, stderr
from random import randrange, random, choice
from time import time

Move = {'U': [0, -1], 'D': [0, 1], 'R': [1, 0], 'L': [-1, 0]}
Positions_type = {'EMPTY': 0, 'WALL': 1, 'AGENT': 5, 'EXIT': 8}

T = 10 ** 10


class Map:
    def __init__(self, map, n, m):
        self.map = map
        self.start_point = self.get_start_point()
        self.size = n * m
        self.n = n
        self.m = m

    def get_start_point(self):
        for i, _ in enumerate(self.map):
            for j, value in enumerate(self.map[i]):
                if value == Positions_type.get('AGENT'):
                    return j, i

    def get_path_cost(self, path):
        x, y = self.start_point
        cost = 0
        for move in path:
            cost += 1
            if cost >= self.size:
                return maxsize

            shift_x, shift_y = Move.get(move)
            if shift_x + x not in range(self.n) or shift_y + y not in range(self.m):
                return maxsize
            if self.map[shift_y + y][shift_x + x] == Positions_type.get('EXIT'):
                break
            if self.map[shift_y + y][shift_x + x] != Positions_type.get('WALL'):
                x, y = x + shift_x, y + shift_y
        return cost

    def init_path(self):
        x, y = self.start_point
        path = []
        max_cost = self.size // 3
        cost = 0

        while True:
            if max_cost < cost:
                x, y = self.start_point
                cost = 0
                path = []
            cost += 1
            neighbors = []
            for key, shift_x_y in Move.items():
                shift_x, shift_y = shift_x_y
                if self.map[shift_y + y][shift_x + x] == Positions_type.get('EXIT'):
                    path.append(key)
                    return path
                if self.map[shift_y + y][shift_x + x] != Positions_type.get('WALL'):
                    neighbors.append(key)
            move = choice(neighbors)
            new_x, new_y = Move.get(move)
            x, y = x + new_x, y + new_y
            path.append(move)


def generate_solution(path, map):
    temp_path = path.copy()
    if random() < 0.3:
        i = randrange(len(temp_path))
        j = randrange(len(temp_path))
        temp_path[i], temp_path[j] = temp_path[j], temp_path[i]
        return temp_path
    if random() < 0.3:
        i = randrange(len(temp_path) - 1)
        j = choice([c for c in range(len(temp_path)) if c > i])
        return temp_path[:i] + list(reversed(temp_path[i:j])) + temp_path[j:]
    temp_path = map.init_path()
    return temp_path


def cooler(t):
    return t * 0.9999


def annealing(map, time_limit):
    temperature = T
    current_solution = map.init_path()
    best_solution = current_solution.copy()
    best_result = map.get_path_cost(best_solution)

    start = time()
    while time() - start < time_limit:
        temp_solution = generate_solution(current_solution, map)
        result = map.get_path_cost(current_solution)
        temp_result = map.get_path_cost(temp_solution)

        if temp_result < result or random() < exp((result - temp_result) / temperature):
            current_solution = temp_solution
            result = temp_result

        if result < best_result:
            best_solution = current_solution
            best_result = result

        temperature = cooler(temperature)

    return best_result, best_solution


def main():
    t, n, m = list(map(int, input().split()))
    mapping = [[int(char) for char in input()[:m]] for _ in range(n)]

    mapp = Map(mapping, n, m)
    best_result, best_solution = annealing(mapp, t)

    print(best_result)
    print("".join(move for move in best_solution[:best_result]), file=stderr)


if __name__ == "__main__":
    main()
