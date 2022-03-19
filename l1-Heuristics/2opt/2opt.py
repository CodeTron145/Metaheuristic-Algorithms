from curses.panel import new_panel
import tsplib95 as tsp
import numpy as np


def two_opt(existing_route, i, k):
    existing_route[i:k] = reversed(existing_route[i:k])

    return existing_route
        

def calc_distance(existing_route, weight_matrix):
    distance = 0 

    for i in range(2, len(existing_route)):
        edge = existing_route[i-1], existing_route[i]
        distance += weight_matrix.get_weight(*edge)

    return distance


def find_best_distance(tsp_file, existing_route): 
    n = len(existing_route)
    weight_matrix = tsp.load(tsp_file)
    best_distance = calc_distance(existing_route, weight_matrix)

    for i in range(1, n):
        for k in range(i+1, n):
            new_route = two_opt(existing_route[:], i, k)
            new_distance = calc_distance(new_route, weight_matrix)
            
            if new_distance < best_distance:
                existing_route = new_route
                best_distance = new_distance
                break

    return best_distance
