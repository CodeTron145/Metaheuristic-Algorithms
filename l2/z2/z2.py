from math import exp
from time import time
from sys import maxsize, stderr
from random import choice, random
from copy import deepcopy

VALUES = [0, 32, 64, 128, 160, 192, 223, 255]

T = 10 ** 10


class Block:
    def __init__(self, start_row, start_column, width, height, value):
        self.start_row = start_row
        self.start_column = start_column
        self.width = width
        self.height = height
        self.value = value


class BlockMatrix:
    def __init__(self, blocks, n, m):
        self.blocks = blocks
        self.n = n
        self.m = m

    def __getitem__(self, key):
        row, column = key
        for block in self.blocks:
            if block.start_row <= row < block.start_row + block.height and block.start_column <= column and block.start_column + block.width > column:
                return block.value
        return -1

    def copy(self):
        return BlockMatrix(deepcopy(self.blocks), self.n, self.m)

    def __repr__(self):
        return '\n'.join(' '.join(str(self[i, j]) for j in range(self.m)) for i in range(self.n))


def generate_matrix(n, m, k):
    blocks = []

    for i in range(0, n - k + 1, k):
        block_height = n - i if i + 2 * k > n else k
        for j in range(0, m - k + 1, k):
            block_width = m - j if j + 2 * k > m else k

            blocks.append(Block(i, j, block_width, block_height, choice(VALUES)))

    return BlockMatrix(blocks, n, m)


def distance(matrix, block_matrix, n, m):
    return (1 / (n * m)) * sum((matrix[i][j] - block_matrix[i, j]) ** 2 for j in range(m) for i in range(n))


def new_value(block_matrix, k):
    temp_matrix = block_matrix.copy()
    block = choice(temp_matrix.blocks)
    block.value = choice(VALUES)
    return temp_matrix


def swap(block_matrix, k):
    temp_matrix = block_matrix.copy()
    block_num_1 = choice(temp_matrix.blocks)
    block_num_2 = choice([b for b in temp_matrix.blocks if b is not block_num_1])
    block_num_1.value, block_num_2.value = block_num_2.value, block_num_1.value
    return temp_matrix


def shift(block_matrix, k):
    try:
        length_gt_k = choice([block for block in block_matrix.blocks if block.width > k and block.start_row == 0])
        width_gt_k = choice([block for block in block_matrix.blocks if block.height > k and block.start_column == 0])
    except IndexError:
        return new_value(block_matrix, k)
    try:
        block_width = choice([block for block in block_matrix.blocks if block.start_row == 0 and block is not length_gt_k])
        block_height = choice([block for block in block_matrix.blocks if block.start_column == 0 and block is not width_gt_k])
    except IndexError:
        return new_value(block_matrix, k)
    
    def by_width(block_matrix):
        temp_matrix = block_matrix.copy()
        if length_gt_k.start_column >block_width.start_column:
            for block in temp_matrix.blocks:
                if block.start_column == length_gt_k.start_column:
                    block.start_column += 1
                    block.width -= 1
            for block in temp_matrix.blocks:
                if block.start_column == block_width.start_column:
                    block.width += 1
            for block in temp_matrix.blocks:
                if block_width.start_column < block.start_column < length_gt_k.start_column:
                    block.start_column += 1
        else:
            for block in temp_matrix.blocks:
                if block.start_column == length_gt_k.start_column:
                    block.width -= 1
            for block in temp_matrix.blocks:
                if block.start_column == block_height.start_column:
                    block.start_column -= 1
                    block.width += 1
            for block in temp_matrix.blocks:
                if block_height.start_column - 1 > block.start_column > length_gt_k.start_column:
                    block.start_column -= 1
        return temp_matrix

    def by_height(block_matrix):
        temp_matrix = block_matrix.copy()
        if width_gt_k.start_row > block_height.start_row:
            for block in temp_matrix.blocks:
                if block.start_row == width_gt_k.start_row:
                    block.start_row += 1
                    block.height -= 1
            for block in temp_matrix.blocks:
                if block.start_row == block_height.start_row:
                    block.height += 1
            for block in temp_matrix.blocks:
                if block_height.start_row < block.start_row < width_gt_k.start_row:
                    block.start_row += 1
        else:
            for block in temp_matrix.blocks:
                if block.start_row == width_gt_k.start_row:
                    block.height -= 1
            for block in temp_matrix.blocks:
                if block.start_row == block_height.start_row:
                    block.start_row -= 1
                    block.height += 1
            for block in temp_matrix.blocks:
                if block_height.start_row - 1 > block.start_row > width_gt_k.start_row:
                    block.start_row -= 1
        return temp_matrix

    shift_kind = choice([by_height, by_width])
    return shift_kind(block_matrix, k)


def generate_solution(block_matrix, k):
    generator = choice([new_value, shift, swap])
    return generator(block_matrix, k)


def cooler(t):
    return t * 0.9999


def annealing(time_limit, matrix, n, m, k):
    temperature = T
    current_solution = generate_matrix(n, m, k)
    best_solution = current_solution
    best_result = distance(matrix, current_solution, n, m)

    start = time()
    while time() - start < time_limit:
        temp_solution = generate_solution(current_solution, k)
        current_result = distance(matrix, current_solution, n, m)
        temp_result = distance(matrix, temp_solution, n, m)

        if temp_result < current_result or random() < exp((current_result - temp_result) / temperature):
            current_solution = temp_solution
            current_result = temp_result

        if current_result < best_result:
            best_solution = current_solution
            best_result = current_result

        temperature = cooler(temperature)

    return best_result, best_solution


def main():
    t, n, m, k = list(map(int, input().split()))
    matrix = [list(map(int, input().split())) for _ in range(n)]

    best_result, best_solution = annealing(t, matrix, n, m, k)

    print(best_result)
    print(best_solution, file=stderr)


if __name__ == "__main__":
    main()
