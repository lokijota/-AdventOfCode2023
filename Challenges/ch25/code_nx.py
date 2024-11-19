import time
from collections import deque
import sys
import numpy as np
import re
import copy
from copy import deepcopy
from tqdm import tqdm
import random
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import networkx as nx

# functions

# main code

# read all the lines
with open('challenges/ch25/input.txt') as f:
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

## part 1
start_time = time.time()
result = 0

n_graphs = 0

# generate a list with all the connections, assuming bi-directionality (i.e., one edge only between each connected node)
edges = []

for node in graph.keys():
    connections = graph[node]

    for connection in connections:
        if (node, connection) not in edges and (connection, node) not in edges:
            edges.append((node, connection))

# instantiate a nx.Graph object
G = nx.Graph()
G.add_edges_from(edges)

cut_edges = nx.minimum_edge_cut(G)

for cut_edge in cut_edges:
    G.remove_edge(cut_edge[0], cut_edge[1])

cc = nx.connected_components(G)
cc = list(cc).copy()

print(f"Graph component 1 size = {len(cc[0])}, Graph component 1 size = {len(cc[1])}")
result = len(cc[0]) * len(cc[1])

print("Result part 1: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))

exit()

# the following code was from a previous solution where I found the nodes to cut from visual inspection
# the previous solution uses https://en.wikipedia.org/wiki/Minimum_cut and 
# https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.connectivity.cuts.minimum_edge_cut.html

print(".------.")

print(f"Node count={G.size()}")

options = {
    'node_color': 'cyan',
    'node_size': 500,
    'width': 1,
    'edge_color': 'green'
}
# subax1 = plt.subplot(111) # the figure has 1 row, 1 columns, and this plot is the first plot.
# nx.draw(G, with_labels=True, font_weight='normal', **options)
# plt.show()

# This shows these are breaking edges to cut, so let's remove them
# rfq - lsk
# zhg - qdv
# gpz - prk

G.remove_edge('rfq', 'lsk')
G.remove_edge('zhg', 'qdv')
G.remove_edge('gpz', 'prk')

# subax1 = plt.subplot(111) # the figure has 1 row, 1 columns, and this plot is the first plot.
# nx.draw(G, with_labels=True, font_weight='normal', **options)
# plt.show()

# ok, this worked. now how many elements are in each of the subgraphs?

cc = nx.connected_components(G)
cc = list(cc).copy()

print(f"Graph component 1 size = {len(cc[0])}, Graph component 1 size = {len(cc[1])}")
result = len(cc[0]) * len(cc[1])

print("Result part 1: ", result) #
print("--- %s seconds ---" % (time.time() - start_time))


# input("*********** Press Enter to continue... **********")
# start_time = time.time()
# print("Result part 2: ", result) #
# print("--- %s seconds ---" % (time.time() - start_time))

