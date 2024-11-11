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

    # if there are nodes that still haven't been visited, the while loop at the top will run
    # for the second graph and so on

    # print(f"Num graphs= {num_graphs}")
    return num_graphs


## part 1
start_time = time.time()
result = 0

n_graphs = 0

while n_graphs != 2:

    graph_iter = copy.deepcopy(graph) # very inneficient but let's see how fast this goes
    nodes = list(graph_iter.keys())
    
    for node1 in nodes:
        for node2 in nodes[1:]:
            for node3 in nodes[1:]:
                print(f"{node1}, {node2}, {node3}")




print("--- %s seconds ---" % (time.time() - start_time))
print("Result part 1: ", result)


## part 2

# input("*********** Press Enter to continue... **********")
# start_time = time.time()
# print("Result part 2: ", result) #
# print("--- %s seconds ---" % (time.time() - start_time))

