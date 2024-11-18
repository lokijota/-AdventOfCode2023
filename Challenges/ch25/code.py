import time
from collections import deque
import sys
import numpy as np
from collections import Counter
import re
import copy
from tqdm import tqdm
import random
import matplotlib.pyplot as plt
import numpy as np

# functions

# main code

# read all the lines
with open('Challenges/ch25/input.txt') as f:
    lines = f.read().splitlines()

# global variables
graph = {}

# process data

# create the graph structure with bidirectional connections
for line in lines:

    nodes = line.split(":")

    src_node = nodes[0]
    target_nodes = nodes[1].strip().split(" ")

    # create the source if it's not there yet
    if src_node not in graph:
        graph[src_node] = set()

    for target_node in target_nodes:
        # add a connection from source to destination
        graph[src_node].add(target_node)

        # create the destination if it doesn't exist yet
        if target_node not in graph:
            graph[target_node] = set()

        # create the reverse direction if it wasn't there yet
        graph[target_node].add(src_node)

# print(graph)

def count_graphs(graph):
    """ Counts the number of disjoint graphs """

    all_nodes = set(graph.keys())
    visited = set()
    num_graphs = 0
    graph_sizes = []

    # while there are unvisited notes, visit all the nodes in a "subgraph"
    while len(all_nodes) > 0:
        head = all_nodes.pop()
        # print(f"Head: {head}")

        if head in visited:
            continue

        connected_nodes = graph[head] - visited
        while len(connected_nodes) > 0:

            # get an element from the set
            elem = connected_nodes.pop()

            # print(f"Visiting node: {elem}")
            connected_nodes = connected_nodes.union(graph[elem])
            visited.add(elem)
            connected_nodes = connected_nodes - visited

        all_nodes = all_nodes - visited
        num_graphs += 1
        graph_sizes.append( len(graph.keys()) - sum(graph_sizes) - len(all_nodes))

        if num_graphs == 3: # bad result let's exit already
            return 3, [0, 0, 0]

    # if there are nodes that still haven't been visited, the while loop at the top will run
    # for the second graph and so on

    # print(f"Num graphs= {num_graphs}")
    return num_graphs, graph_sizes

def cut_vertex(graph, vertex):
    """ Remove a vertex from the graph """

    # should never happen
    if vertex[0] not in graph or vertex[1] not in graph:
        return graph
    
    graph[vertex[0]].discard(vertex[1])
    graph[vertex[1]].discard(vertex[0])

    return graph

def add_vertex(graph, vertex):
    """ Add a vertex from the graph """

    graph[vertex[0]].add(vertex[1])
    graph[vertex[1]].add(vertex[0])

    return graph


## part 1
start_time = time.time()
result = 0

n_graphs = 0

# generate a list with all the connections, assuming bi-directionality
vertices = []

for node in graph.keys():
    connections = graph[node]

    for connection in connections:
        if (node, connection) not in vertices and (connection, node) not in vertices:
            vertices.append((node, connection))

# print(vertices, len(vertices))

# print(count_graphs(graph))
# print("--- %s seconds ---" % (time.time() - start_time))
# 0.29 - 0.30 secs per graph

for idx1, vertex1 in enumerate(vertices):
    delta2 = idx1+1
    print(idx1, end=", ")
    for vertex2 in vertices[idx1+delta2:]:
        delta2 += 1
        print((time.time() - start_time))
        delta3 = delta2

        for vertex3 in vertices[idx1+delta3:]:
            delta3 = delta2+1
            # print(vertex1, vertex2, vertex3)

            graph = cut_vertex(graph, vertex1)
            graph = cut_vertex(graph, vertex2)
            graph = cut_vertex(graph, vertex3)

            n_graphs, subgraph_node_counts = count_graphs(graph) 
            if n_graphs == 2:
                print(vertex1, vertex2, vertex3, subgraph_node_counts)

                result = subgraph_node_counts[0] * subgraph_node_counts[1]

                print("--- %s seconds ---" % (time.time() - start_time))
                print("Result part 1: ", result)
                exit()

            graph = add_vertex(graph, vertex1)
            graph = add_vertex(graph, vertex2)
            graph = add_vertex(graph, vertex3)



# 1492 is too low

## part 2

# input("*********** Press Enter to continue... **********")
# start_time = time.time()
# print("Result part 2: ", result) #
# print("--- %s seconds ---" % (time.time() - start_time))

