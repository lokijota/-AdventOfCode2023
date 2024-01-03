import copy
import numpy as np
import random
import re
import sys
import time
import heapq
from numba import njit
from tqdm import tqdm
from collections import Counter, deque

# main code

# read all the lines
with open('Challenges/ch17/input.txt') as f:
    lines = f.read().splitlines()

# parse data file content

nrows = len(lines)
ncols = len(lines[0])
map = [[int(i) for i in row] for row in lines]
map = np.array(map)

# global variables

# weight of a given path, nodes it's been through
paths = [ [0 , [[0,0]]] ] # start with weight 0, as first square doesn't count

# functions

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printPath(map, path):
    "Print out the map with the path followed in colour"
    for r in range(0, nrows):
        for c in range(0, ncols):
            if [r,c] in [[node[0],node[1]] for node in path]:
                print(f"{bcolors.OKGREEN}{map[r][c]}{bcolors.ENDC}", end="")
            else:
                print(map[r][c], end="")
        print()


def get_possible_next_nodes(current_min_node, minSteps, maxSteps):
    "Returns all possible next nodes, for all possible movement directions considering the current node"

    if current_min_node[0] == 0 and current_min_node[1] == 0:
        if current_min_node[2] == "X": # start node
            vert = [(sum(map[current_min_node[0]+1:current_min_node[0]+j, current_min_node[1]]),(current_min_node[0]+j ,current_min_node[1],"S")) for j in range(minSteps, maxSteps+1)]
            horz = [(sum(map[current_min_node[0], current_min_node[1]+1:current_min_node[1]+j]),(current_min_node[0],current_min_node[1]+j,"E")) for j in range(minSteps, maxSteps+1)]
            return vert + horz
        else:
            return [] #repeat visits to 0,0 make no sense

    elif current_min_node[2] in ["E", "W"]:
        vertN = []
        vertS = []

        # North
        if current_min_node[0] >= minSteps:
            real_max = min(maxSteps, current_min_node[0])
            vertN = [(sum(map[current_min_node[0]-j:current_min_node[0]-1, current_min_node[1]]),(current_min_node[0]-j ,current_min_node[1],"N")) for j in range(minSteps, real_max+1)]

        # South
        if current_min_node[0] <= nrows - minSteps: 
            real_max = min(maxSteps, nrows-1-current_min_node[0])
            vertS = [(sum(map[current_min_node[0]+1:current_min_node[0]+j, current_min_node[1]]),(current_min_node[0]+j ,current_min_node[1],"S")) for j in range(minSteps, real_max+1)]

        return vertN + vertS

    else: # current_min_node[2] in ["N", "S"]:
        horzE = []
        horzW = []

        # East
        if current_min_node[1] <= ncols - minSteps: 
            real_max = min(maxSteps, ncols-1-current_min_node[1])
            horzE = [(sum(map[current_min_node[0], current_min_node[1]+1:current_min_node[1]+j]),(current_min_node[0],current_min_node[1]+j,"E")) for j in range(minSteps, real_max+1)]

        # West
        if current_min_node[1] >= minSteps:
            real_max = min(maxSteps, current_min_node[1])
            horzW = [(sum(map[current_min_node[0], current_min_node[1]-j:current_min_node[1]-1]),(current_min_node[0],current_min_node[1]-j,"W")) for j in range(minSteps, real_max+1)]

        return horzE + horzW

    assert True, "I should not be here"


def dijkstra_algorithm_with_priority_queue(graph, start_node):
    shortest_path = {}
    previous_nodes = {}

    shortest_path[start_node] = 0

    nodes_to_visit = [(0, start_node)]
    heapq.heapify(nodes_to_visit)

    while nodes_to_visit:

        # get node with the lowest score
        _, current_min_node = heapq.heappop(nodes_to_visit)
        print(current_min_node)

        # let's get the neighbours
        neighbors = get_possible_next_nodes(current_min_node, 4, 10)

        for travelcost, neighbor in neighbors: # eg, (13, (5,0,"S"))
            
            # se peso menor, actualizar
            tentative_value = shortest_path[current_min_node] + travelcost

            # se n tiver já sido visitado, meter no queue
            if neighbor not in previous_nodes:
                heapq.heappush(nodes_to_visit, (tentative_value, neighbor))

            if tentative_value < shortest_path.get(neighbor, sys.maxsize):
                shortest_path[neighbor] = tentative_value
                previous_nodes[neighbor] = current_min_node

    return previous_nodes, shortest_path 



def dijkstra_algorithm(graph, start_node):
    "Applies Dijkstra's shortest path algorithm"
    unvisited_nodes = list(graph.get_nodes())
 
    # We'll use this dict to save the cost of visiting each node and update it as we move along the graph   
    shortest_path = {}
 
    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes = {}
 
    # We'll use max_value to initialize the "infinity" value of the unvisited nodes   
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    # However, we initialize the starting node's value with 0   
    shortest_path[start_node] = 0
    
    # The algorithm executes until we visit all nodes
    # JOTA edit
    pbar = tqdm(total=len(unvisited_nodes)+1)
    # JOTA end edit

    while unvisited_nodes:
        # The code block below finds the node with the lowest score
        current_min_node = None
        for node in unvisited_nodes: # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
        
        # The code block below retrieves the current node's neighbors and updates their distances
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            # JOTA edit - prevent revisiting nodes
            if current_min_node in previous_nodes:
                prev_visited_node = previous_nodes[current_min_node]
                if prev_visited_node[0] == neighbor[0] and prev_visited_node[1] == neighbor[1]:
                    continue
            # JOTA end edit
            
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node

        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)
        pbar.update(1) # JOTA added
    
    pbar.close() # JOTA added

    return previous_nodes, shortest_path

def print_result(previous_nodes, shortest_path, start_node, target_node):
    "Auxiliary function to print the path and map in a convenient way and returns the sum of the cost"
    path = []
    node = target_node
    
    while node != start_node:
        path.append(node)
        node = previous_nodes[node]
 
    # Add the start node manually
    path.append(start_node)
    
    print("We found the following best path with a value of {}.".format(shortest_path[target_node]))
    print(" -> ".join(reversed([''.join(i) for i in [str(i) for i in path]])))
    printPath(map, path)

    return shortest_path[target_node]

# process data
# part 2

result = 0
start_time = time.time()

previous_nodes, shortest_path = dijkstra_algorithm_with_priority_queue(graph=None, start_node=(0,0, "X"))

# as we have 2 end nodes, we have to find the one with the lowest cost, to print the result
min_node = None
min_dist = 99999999
for p in shortest_path:
    if p[0] == nrows-1 and p[1] == ncols-1 and p[2] in ["S", "E"]:
        if shortest_path[p] < min_dist:
            min_dist = shortest_path[p]
            min_node = p
assert min_dist != 99999999, "Path not found!"

print("Node with lowest cost:", min_node, "Cost:", min_dist)

result = print_result(previous_nodes, shortest_path, start_node=(0,0, "X"), target_node=min_node)

print(len(previous_nodes), len(shortest_path))
print("Result part 2: ", result) 
print("--- %s seconds ---" % (time.time() - start_time))


# Result part 2:  1416
# --- 27427.103300094604 seconds ---
# ^right answer after 7.6 hours!... not good. I had a bug and was only doing 9 in a row and not 10.

# 1152 -- muito baixo, n está a calcular bem
