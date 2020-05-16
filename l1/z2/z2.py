import random
import sys
from time import time


def generate_dictionary(path):
    with open(path, 'r') as length_data:
        content = length_data.readlines()

    distances = list(content)[1:]

    neighbours_dict = {}
    for i in distances:
        neighbours_dict[distances.index(i)] = list(map(int, i.split()))

    return neighbours_dict


def generate_solution(neighbours_dir):
    current_node = 0

    solution = [current_node]
    while 0 not in solution[1:]:
        arr = neighbours_dir[current_node]
        minimum = max(arr)
        ind = 0
        for i in range(len(arr)):
            if arr[i] < minimum and i not in solution:
                minimum = arr[i]
                ind = i
            elif minimum == max(arr) and i not in solution:
                ind = i

        solution.append(ind)
        current_node = ind

    return solution


def generate_neighbour(solution):
    neighbour = solution
    generated = True
    while generated:
        city_index1 = random.randint(0, len(neighbour) - 3)
        city_index2 = random.randint(0, len(neighbour) - 3)
        if city_index1 != city_index2:
            tmp = neighbour[city_index1 + 1]
            neighbour[city_index1 + 1] = solution[city_index2 + 1]
            neighbour[city_index2 + 1] = tmp
            generated = False

    return neighbour


def distance(solution, neighborhood_dict):
    distance = 0
    for i in range(len(solution)):
        if i == len(solution) - 1:
            break
        for j in neighborhood_dict.keys():
            if solution[i + 1] == j:
                distance += neighborhood_dict[solution[i]][j]

    return distance


def tabu_search(dictionary, first_solution, max_time):
    start_time = time()
    tabu_list = []
    best = first_solution
    best_candidate = best.copy()
    while time() - start_time < max_time:

        s_neighbours = generate_neighbour(best)
        if s_neighbours not in tabu_list and distance(s_neighbours, dictionary) < distance(best_candidate, dictionary):
            best_candidate = s_neighbours.copy()
            tabu_list.append(best_candidate)
        if distance(best_candidate, dictionary) < distance(best, dictionary):
            best = best_candidate.copy()
        if len(tabu_list) > 5:
            tabu_list.remove(tabu_list[1])

    return str(distance(best, dictionary)) + "\n" + " ".join(str(elem) for elem in best)


def main():
    with open(sys.argv[1], 'r') as in_data:
        content = in_data.readline().split()

    dictionary = generate_dictionary(sys.argv[1])
    first_solution = generate_solution(dictionary)
    result = tabu_search(dictionary, first_solution, float(content[0]))
    print("Result in output.txt!")

    with open(sys.argv[2], 'w') as out_data:
        content = out_data.write(result)


main()
