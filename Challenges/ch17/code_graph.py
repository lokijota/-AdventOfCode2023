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
# paths = [ [int(map[0][0]) , [[0,0]]] ]
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

    for r in range(0, nrows):
        for c in range(0, ncols):
            if [r,c] in [[node[0],node[1]] for node in path]: #path[2:]:
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
        
    def construct_graph(self, nodes, init_graph):
        '''
        This method makes sure that the graph is symmetrical.
        In other words, if there's a path from node A to B with a value V,
        there needs to be a path from node B to node A with a value V.
        '''
        graph = {}
        for node in nodes:
            graph[node] = {}
        
        graph.update(init_graph)
        
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
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections
    
    def value(self, node1, node2):
        "Returns the value of an edge between two nodes."
        return self.graph[node1][node2]

def direction(sourceNode, targetNode):
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
    
    return "banana"

def dijkstra_algorithm(graph, start_node):
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
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node
 
        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)
    
    return previous_nodes, shortest_path

def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node
    
    while node != (0, 0, 'X', 0): #start_node[:2]:
        path.append(node)
        node = previous_nodes[node]
 
    # Add the start node manually
    path.append(start_node)
    # print(path)
    
    print("We found the following best path with a value of {}.".format(shortest_path[target_node]))
    print(" -> ".join(reversed([''.join(i) for i in [str(i) for i in path]])))
    printPath(map, path)

    return shortest_path[target_node]

def generateSurroundingPositions(pos):
    surroundingPositions = []

    # order is relevant. what I put in the end is explored first.

    if pos[1] > 0: # and pos[0] != nrows-1:
        surroundingPositions.append([pos[0], pos[1]-1])

    if pos[0] > 0: # and pos[1] != ncols-1:
        surroundingPositions.append([pos[0]-1, pos[1]])
    
    if pos[1]+1 < ncols:
        surroundingPositions.append([pos[0], pos[1]+1])

    if pos[0]+1 < nrows:
        surroundingPositions.append([pos[0]+1, pos[1]])

    return surroundingPositions

# process data

# part 1

result = 0

start_time = time.time()

# 1.0 create graph
nodes = []
init_graph = {}
for node in nodes:
    init_graph[node] = {}

for r in range(0,nrows):
    for c in range(0,ncols):

        # a. create the nodes

        # a.1 start node is special
        if r == c == 0:
            nodes.append((0,0,"X", 0))
            init_graph[(0,0,"X", 0)] = {}
            continue

        # a.2 but the other nodes are vulgar nodes
        for dir in ["N", "S", "E", "W"]:
            for stepCount in range(0,4):
                currentNodeKey = (r,c, dir, stepCount)
                nodes.append(currentNodeKey)
                init_graph[currentNodeKey] = {}

print("Nb of Nodes:", len(init_graph))
# b. create the connections
        
unprocessed = [(0,0,"X", 0)]

vertexCount = 0

while unprocessed:
    
    current = unprocessed.pop()

    adjacentPositions = generateSurroundingPositions([current[0],current[1]])
    for adjPos in adjacentPositions:
        # from -> to = distance

        if adjPos == [0,0]: # or adjPos == [12,12]:
            continue

        dir = direction((current[0], current[1]), adjPos)

        if current == (0,0,"X",0):
            destination = (adjPos[0], adjPos[1], dir, current[3]+1)

            if destination not in init_graph[current]:
                init_graph[current][destination] = int(map[adjPos[0]][adjPos[1]])
                unprocessed.append(destination)

        elif current[2] == dir and current[3] == 3:
            # don't create connection -- same direction and we're already at 3
            continue

        elif current[2] == dir:
            destination = (adjPos[0], adjPos[1], dir, current[3]+1)

            if destination not in init_graph[current]:
                init_graph[current][destination] = int(map[adjPos[0]][adjPos[1]])
                unprocessed.append(destination)

        elif current[2] != dir:
            destination =  (adjPos[0], adjPos[1], dir, 1)
            if destination not in init_graph[current]:
                init_graph[current][destination] = int(map[adjPos[0]][adjPos[1]])
                unprocessed.append(destination)

        vertexCount += 1
    
# print(init_graph)
print("Graph created, vertices =", vertexCount)


graph = Graph(nodes, init_graph)
previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=(0,0, "X", 0))

print("---------")

minNode = None
minDist = 99999999
for p in shortest_path:
    if p[0] == 12 and p[1] == 12 and p[2] in ["S", "E"]:
        # print("SP:", p, "Dist:", shortest_path[p])
        if shortest_path[p] < minDist:
            minDist = shortest_path[p]
            minNode = p

print("Min:", minNode, "Dist:", minDist)

print("########")

# print(previous_nodes)
# print(shortest_path)

result = print_result(previous_nodes, shortest_path, start_node=(0,0, "X", 0), target_node=minNode) #(nrows-1,ncols-1))


# result = findShortestPath(map, paths)

print("Result part 1: ", result) # part 1 - 6906
print("--- %s seconds ---" % (time.time() - start_time))

# 2419 is too high /  Found new mininum: 2419 / secs: 37212.687748909
# 1559 is too high Found new mininum: 1559 / secs: 157.61041522026062 len(paths):  405 len(path): 318
# djk maggie diz 1302 is wrong
# 1261 É O VALOR CERTO

# part 2

result = -1

start_time = time.time()
print("Result part 2: ", result) 
print("--- %s seconds ---" % (time.time() - start_time))
