import math
import tsplib95 as tsp

def logCalc(x1,x2,y1,y2):
    dist = math.sqrt(math.pow(x2-x1,2) + math.pow(y2-y1,2))
    return dist

def nearest_neighbour_finder(tsp_file, start_point):
    problem = tsp.load(tsp_file)
    starting_point = start_point

    sum_dist = 0
    min_id = starting_point
    tryRoute = [starting_point]
    temp = starting_point
    for i in range(1, len(list(problem.get_nodes()))):
        min_dist = 10000
        for j in range(1, len(list(problem.get_nodes())) + 1):
            exist = 0
            if temp == j:
                continue
            for k in range(0, len(tryRoute)):
                if j == tryRoute[k]:
                    exist = 1
            if exist == 1:
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
    return tryRoute, sum_dist

