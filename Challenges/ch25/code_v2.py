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

def count_graphs(graph):
    """ counts the number of disjoint graphs """

    all_nodes = set(graph.keys())
    visited = set()
    num_graphs = 0
    graph_sizes = []

    # while there are unvisited notes, visit all the nodes in a "subgraph"
    while len(all_nodes) > 0:
        head = all_nodes.pop()
        # print(f"head: {head}")

        if head in visited:
            continue

        connected_nodes = graph[head] - visited
        while len(connected_nodes) > 0:

            # get an element from the set
            elem = connected_nodes.pop()

            # print(f"visiting node: {elem}")
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

    # print(f"num graphs= {num_graphs}")
    return num_graphs, graph_sizes

def cut_edge(graph, edge):
    """ remove an edge from the graph """

    # should never happen
    # if edge[0] not in graph or edge[1] not in graph:
    #     return graph
    
    graph[edge[0]].discard(edge[1])
    graph[edge[1]].discard(edge[0])

    return graph

def add_edge(graph, edge):
    """ add an edge to the graph """

    graph[edge[0]].add(edge[1])
    graph[edge[1]].add(edge[0])

    return graph

## disjoint set union
## https://www.geeksforgeeks.org/number-of-connected-components-of-a-graph-using-disjoint-set-union/
## this code is contributed by shivam dwivedi

# function to find the topmost parent of vertex x
def find(x):
  if x != parent[x]:
    parent[x] = find(parent[x])
  return parent[x]

def union(x,y):
  parent_x = find(x)
  parent_y = find(y)
  if parent_x != parent_y:
    parent[parent_y] = parent_x
  
## part 1
start_time = time.time()
result = 0

n_graphs = 0

# generate a list with all the connections, assuming bi-directionality (i.e., one edge only between each connected node)
edges = []
edges_clone = []

for node in graph.keys():
    connections = graph[node]

    for connection in connections:
        if (node, connection) not in edges and (connection, node) not in edges:
            edges.append((node, connection))
            edges_clone.append((node, connection))

# print(edges, len(edges))

# stores the parent of each vertex, initialized with itself
parent_original = dict(zip(graph.keys(), graph.keys())) 

# for x,y in edges:
#   union(x,y)

# dict_pair = defaultdict(list)

# for idx, val in enumerate(parent):
#   dict_pair[find(val)].append(idx)

# print(len(dict_pair.keys()))

# print("--- %s seconds ---" % (time.time() - start_time))

print("----------------------------------------------------------")

# print(parent)

# ordenar as edges com os nós que têm menos ligações primeiro?
edges.sort(key=lambda x: len(graph[x[0]]) + len(graph[x[1]]))

for idx1, vertex1 in enumerate(edges):
    delta2 = idx1+1
    print(idx1)
    for vertex2 in edges[idx1+delta2:]:
        delta2 += 1
        print(idx1, delta2, (time.time() - start_time))
        start_time = time.time()

        delta3 = delta2
        for vertex3 in edges[idx1+delta3:]:
            delta3 = delta2+1
            # print(edge1, edge2, edge3)

            # remove the edge from the edge clone
            # print(f"e: {edges}")
            # print(f"ec: {edges_clone}")
            # print(f"edges to remove: ", vertex1, vertex2, vertex3)

            start_time = time.time()
            edges_clone.remove(vertex1)
            edges_clone.remove(vertex2)
            edges_clone.remove(vertex3)
            print("  --- clones:", (time.time() - start_time)*100)

            # edges to remove:  ('jqt', 'nvd') ('pzl', 'hfx') ('cmg', 'bvb')

            # now set the parents for all the 3 edges to itself in the parent structure
            # surrounding_nodes = set()
            # surrounding_nodes.add(vertex1[0])
            # surrounding_nodes.add(vertex1[1])
            # surrounding_nodes.add(vertex2[0])
            # surrounding_nodes.add(vertex2[1])
            # surrounding_nodes.add(vertex3[0])
            # surrounding_nodes.add(vertex3[1])

            # print(len(surrounding_nodes))

            # for sn in surrounding_nodes:
            #     parent[sn] = sn

            # # now do the needed unions for the other nodes in these surrounding nodes
            # for a, b in [(x,y) for x,y in edges_clone if x in surrounding_nodes or y in surrounding_nodes]:
            #     union(a,b)

            start_time = time.time()
            parent = dict(zip(graph.keys(), graph.keys())) 
            print("  --- dict/zip:", (time.time() - start_time)*100)
            # jota: ganho alguma coisa se inicializar com um valor diferente? tipo o topo mais comum. acho que destroi o union()

            # jota: e se guardar a árvore no caminho upward? assumindo qeu é uma árvore na repr original, sem circularidades

            # parent = deepcopy(parent_original) -- worse performance
            
            start_time = time.time()
            for x,y in edges_clone:
                union(x,y)
            print("  --- unions:", (time.time() - start_time)*100)
 
            # now count
            dict_pair = defaultdict(list) # a subclass of the built-in dict class and provides a default value for the key that does not exist

            start_time = time.time()
            for idx, val in enumerate(parent):
                dict_pair[find(val)].append(idx)
            print("  --- find/append:", (time.time() - start_time)*100)

            start_time = time.time()
            n_graphs = len(dict_pair.keys())
            print("  --- len/keys:", (time.time() - start_time)*100)

            if n_graphs == 2:
                print("Vertices to cut: ", vertex1, vertex2, vertex3)
                print("Parent: ", parent)
                print("--- %s seconds ---" % (time.time() - start_time))
                print("Result part 1: ", result)
                exit()
            # elif n_graphs > 2:
            #     print(f"PUMBA {n_graphs}") 
            # else:
            #     print(f"Graph count: {n_graphs}")

            # put it there again
            edges_clone.append(vertex1)
            edges_clone.append(vertex2)
            edges_clone.append(vertex3)

            # don't need the graph anymore
            # graph = cut_edge(graph, vertex1)
            # graph = cut_edge(graph, vertex2)
            # graph = cut_edge(graph, vertex3)

            # tenho de trocar isto pelo disjoint set. mas consigo evitar chamadas repetidas? tudo o quero é ir removendo do edges, na verdade é equivalente ao grafo.
            # tudo das hashtables é inútil
            # n_graphs, subgraph_node_counts = count_graphs(graph) 
            # if n_graphs == 2:
            #     print(vertex1, vertex2, vertex3, subgraph_node_counts)

            #     result = subgraph_node_counts[0] * subgraph_node_counts[1]

            #     print("--- %s seconds ---" % (time.time() - start_time))
            #     print("Result part 1: ", result)
            #     exit()

            # graph = add_edge(graph, vertex1)
            # graph = add_edge(graph, vertex2)
            # graph = add_edge(graph, vertex3)



# 1492 is too low

## part 2

# input("*********** Press Enter to continue... **********")
# start_time = time.time()
# print("Result part 2: ", result) #
# print("--- %s seconds ---" % (time.time() - start_time))

