import sys
import tsplib95 as tsp

def nearest_neighbour_finder(tsp_file, start_point):
    problem = tsp.load(tsp_file)
    starting_point = start_point

    sum_dist = 0
    min_id = starting_point
    tryRoute = [starting_point]
    temp = starting_point
    for i in range(1, len(list(problem.get_nodes()))):
        min_dist = sys.maxsize
        for j in range(1, len(list(problem.get_nodes())) + 1):
            exist = 0
            if temp == j:
                continue
            if j in tryRoute:
                continue
            edge = temp, j
            dist = problem.get_weight(*edge)
            if dist < min_dist:
                min_dist = dist
                min_id = j
        sum_dist += min_dist
        tryRoute.append(min_id)
        temp = min_id

    edge = min_id, starting_point
    sum_dist += problem.get_weight(*edge)
    tryRoute.append(starting_point)
    return tryRoute

def route_distance(tsp_file, route):
    problem = tsp.load(tsp_file)
    distance = 0
    for i in range(1, len(route)):
        edge = route[i-1], route[i]
        distance += problem.get_weight(*edge)
    return distance
    edge = min_id, starting_point
    sum_dist += problem.get_weight(*edge)
    tryRoute.append(starting_point)
    return tryRoute, sum_dist

