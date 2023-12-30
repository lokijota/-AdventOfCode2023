import numpy as np
from collections import Counter
import re
import copy
from tqdm import tqdm
import time
from collections import deque
import random
import sys

# functions

# main code

# read all the lines
with open('Challenges/ch17/input.txt') as f:
    lines = f.read().splitlines()

# parse data file content

nrows = len(lines)
ncols = len(lines[0])
map = lines

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

###### https://www.udacity.com/blog/2021/10/implementing-dijkstras-algorithm-in-python.html
###### As in last year, trying Dijkstra

class Graph(object):
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)
        # self.outgoingedgescache = {}
        
    def construct_graph(self, nodes, init_graph):
        '''
        This method makes sure that the graph is symmetrical.
        In other words, if there's a path from node A to B with a value V,
        there needs to be a path from node B to node A with a value V.
        JOTA: COMMENTED CODE FOR THE BEHAVIOUR ABOVE -- DON'T WANT THINGS TO BE REVERSIBLE
        '''
        graph = {}
        for node in nodes:
            graph[node] = {}
        
        graph.update(init_graph)
        
        # JOTA edit -- commented to NOT make the graph reversible / that messes up the logic as each node has r,c plus direction + nb of repetitions as ID
        # for node, edges in graph.items():
        #     for adjacent_node, value in edges.items():
        #         if graph[adjacent_node].get(node, False) == False:
        #             graph[adjacent_node][node] = value
                    
        return graph
    
    def get_nodes(self):
        "Returns the nodes of the graph."
        return self.nodes
    
    def get_outgoing_edges(self, node):
        "Returns the neighbors of a node."
        connections = []

        # Jota - small effect not worth it
        # cachekey = str(node[0]) + "_" + str(node[1]) + node[2] + str(node[3])
        # if cachekey in self.outgoingedgescache:
        #     return self.outgoingedgescache[cachekey]

        for out_node in self.nodes:
            # JOTA added "node in self.graph and" because of the cleanup() addition 
            if node in self.graph and self.graph[node].get(out_node, False) != False:
                connections.append(out_node)

        # self.outgoingedgescache[cachekey] = connections
        return connections
    
    def value(self, node1, node2):
        "Returns the value of an edge between two nodes."
        return self.graph[node1][node2]

    def cleanup(self):
        "Jota - Auxiliary method to clean-up nodes that have no connections, from the graph and node base -- makes dijkstra faster"
        self.graph = {k: v for k, v in self.graph.items() if len(v) > 0}
        self.nodes = [node for node in self.nodes if node in self.graph.keys()]

def direction(sourceNode, targetNode):
    "Returns the cardinal direction when you go from the source to the target node"
    if sourceNode[0] == targetNode[0]:
        if sourceNode[1] == targetNode[1]+1:
            return "W"
        elif sourceNode[1] == targetNode[1]-1:
            return "E"
    else: # node1[1] == node2[1]
        if sourceNode[0] == targetNode[0]-1:
            return "S"
        elif sourceNode[0] == targetNode[0]+1:
            return "N"
    
    # otherwise / should never happens
    assert False, "Shouldn't get here"

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
        
        # if shortest_path[current_min_node] > 1687:
        #         continue
        # min = 1687
        # manhattanDistanceToEnd = nrows - current_min_node[0] + ncols - current_min_node[1] -2
        # if shortest_path[current_min_node] +  manhattanDistanceToEnd*2 > min:
        # if shortest_path[current_min_node] > min:
        #     unvisited_nodes.remove(current_min_node)
        #     pbar.update(1) # JOTA added
        
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

            # JOTA edit - this was an attempt at early termination but has the same result but takes more time (300 secs more for the input)
            # if neighbor[0] == nrows -1 and neighbor[1] == ncols - 1:
            #     print("pim achei-lo", tentative_value)
            #     return previous_nodes, shortest_path
 
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

# Implemented a cache that has an abt 10% impact with the final dataset
surroundingPositionsCache = {}

def generateSurroundingPositions(pos):
    "Returns a list with the coordinates surrounding the passed position, in (row,column) format."
    surroundingPositions = []

    cachekey = str(pos[0]) + "_" + str(pos[1])
    if cachekey in surroundingPositionsCache:
        return surroundingPositionsCache[cachekey]
    
    # order is relevant for the exploration, at least in part 1. What is added last is explored first.

    if pos[1] > 0: # and pos[0] != nrows-1:
        surroundingPositions.append([pos[0], pos[1]-1])

    if pos[0] > 0: # and pos[1] != ncols-1:
        surroundingPositions.append([pos[0]-1, pos[1]])
    
    if pos[1]+1 < ncols:
        surroundingPositions.append([pos[0], pos[1]+1])

    if pos[0]+1 < nrows:
        surroundingPositions.append([pos[0]+1, pos[1]])

    surroundingPositionsCache[cachekey] = surroundingPositions
    return surroundingPositions

def oppositeDirection(dir):
    if dir == "S":
        return "N"
    if dir == "N":
        return "S"
    if dir == "E":
        return "W"
    if dir == "W":
        return "E"
    
    assert False, "Shouldn't get here"

def moveInDirByNSteps(map, pos, dir, nsteps):
    "Move by nsteps in direction dir. Returns None if out of bounds. Specific for part 2"
    cost = 0

    if dir == "N" and pos[0]-nsteps+1>=0 and pos[1] > 0: #3rd condition to avoid going back to 0,0
        for j in range(0, nsteps):
            cost += int(map[pos[0]-j][pos[1]])

        return cost,(pos[0]-nsteps+1, pos[1])

    if dir == "S" and pos[0]+nsteps-1 < nrows:
        for j in range(0, nsteps):
            cost += int(map[pos[0]+j][pos[1]])

        return cost, (pos[0]+nsteps-1, pos[1])

    if dir == "W" and pos[1]-nsteps+1>=0 and pos[0] > 0: #3rd condition to avoid going back to 0,0
        for j in range(0, nsteps):
            cost += int(map[pos[0]][pos[1]-j])
        
        return cost, (pos[0], pos[1]-nsteps+1)

    if dir == "E" and pos[1]+nsteps-1 < ncols:
        for j in range(0, nsteps):
            cost += int(map[pos[0]][pos[1]+j])

        return cost, (pos[0], pos[1]+nsteps-1)
    
    return 0, None

# process data
# part 2

result = 0
start_time = time.time()

# 1.0 create graph data structure and its connections
nodes = []
init_graph = {}
for node in nodes:
    init_graph[node] = {}

for r in range(0,nrows):
    for c in range(0,ncols):

        # 1.1 create the nodes

        # start node is special
        if r == c == 0:
            nodes.append((0,0,"X", 0))
            init_graph[(0,0,"X", 0)] = {}
            continue

        # but the other nodes are vulgar nodes, zé-nobodies
        for dir in ["N", "S", "E", "W"]:
            for stepCount in range(0,10): # note change here from part 1: 4 --> 10
                currentNodeKey = (r,c, dir, stepCount)
                nodes.append(currentNodeKey)
                init_graph[currentNodeKey] = {}

print("Nb of Nodes:", len(init_graph))

# 1.2 Create the connections (edges)        
unprocessed = [(0,0,"X", 0)]
edgeCount = 0

while unprocessed:
    current = unprocessed.pop()

    adjacentPositions = generateSurroundingPositions([current[0],current[1]])
    for adjPos in adjacentPositions:
        # from -> to in direction dir => distance/cost

        # JOTA OPTIMIZATION HERE
        if int(map[adjPos[0]][adjPos[1]]) >= 6:
            continue

        # if (adjPos[0] >= 142/2 -14*4 and adjPos[0] <= 142/2 + 14*4) and \
        #    (adjPos[1] >= 142/2 -14*4 and adjPos[1] <= 142/2 + 14*4):
        #     continue

        if adjPos == [0,0]:
            continue

        dir = direction((current[0], current[1]), adjPos)

        if current == (0,0,"X",0):
            costOfJump, nextPos = moveInDirByNSteps(map, adjPos, dir, 4)
            destination = (nextPos[0], nextPos[1], dir, 4)

            if destination not in init_graph[current]:
                init_graph[current][destination] = costOfJump
                unprocessed.append(destination)
            
        elif current[2] == oppositeDirection(dir):
            continue

        elif current[2] == dir and current[3] == 9: # JOTA: Change from part 1 to part 2, 3-->9
            # don't create connection -- same direction and we're already at 3 (i.e., 9 for part 2)
            continue

        elif current[2] == dir:
            destination = (adjPos[0], adjPos[1], dir, current[3]+1)

            if destination not in init_graph[current]:
                init_graph[current][destination] = int(map[adjPos[0]][adjPos[1]])
                unprocessed.append(destination)

        elif current[2] != dir:

            # change of direction, let's more 4
            costOfJump, nextPos = moveInDirByNSteps(map, adjPos, dir, 4)
            if nextPos is None: # out of bounds
                continue
            
            destination = (nextPos[0], nextPos[1], dir, 4)

            if destination not in init_graph[current]:
                init_graph[current][destination] = costOfJump
                unprocessed.append(destination)

        edgeCount += 1
    
print("Graph created, edges =", edgeCount)


graph = Graph(nodes, init_graph)
graph.cleanup()
print("After cleanup, #nodes", len(graph.nodes))
previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=(0,0, "X", 0))

# as we have 16 end nodes, we have to find the one with the lowest cost, to print the result
minNode = None
minDist = 99999999
for p in shortest_path:
    if p[0] == nrows-1 and p[1] == ncols-1 and p[2] in ["S", "E"]:
        if shortest_path[p] < minDist:
            minDist = shortest_path[p]
            minNode = p
assert minDist != 99999999, "Path not found!"

print("Node with lowest cost:", minNode, "Cost:", minDist)

result = print_result(previous_nodes, shortest_path, start_node=(0,0, "X", 0), target_node=minNode) #(nrows-1,ncols-1))

print("Result part 2: ", result) 
print("--- %s seconds ---" % (time.time() - start_time))

# 1523 is too high, com esta condição a evitar pôr nós no grafo -- mas demorou "apenas" 30mins
# if (adjPos[0] >= 142/2 -14*4 and adjPos[0] <= 142/2 + 14*4) and \
# (adjPos[1] >= 142/2 -14*4 and adjPos[1] <= 142/2 + 14*4):
#     continue