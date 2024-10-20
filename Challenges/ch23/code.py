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

def print_map(map, path):
	"""Trivial helper -- print the map - will evolve it later to overlay a path"""
	for row_index, row in enumerate(map):
		for col_index, col in enumerate(row):
			if (row_index, col_index) in path:
				print("O", end="")	
			else:
				print(map[row_index][col_index], end="")

		print()

def next_positions(map, pos, visited):
	# print(">>> ", pos, visited)

	next_pos = set() 
	r = pos[0]
	c = pos[1]

	if map[r][c] == "<":
		next_pos.add((r, c-1))
	elif map[r][c] == ">":
		next_pos.add((r, c+1))
	elif map[r][c] == "^":
		next_pos.add((r-1, c))
	elif map[r][c] == "v":
		next_pos.add((r+1, c))
	else:
		if map[r][c+1] != "#":
			next_pos.add((r, c+1))

		if map[r][c-1] != "#":
			next_pos.add((r, c-1))

		if map[r-1][c] != "#":
			next_pos.add((r-1, c))

		if map[r+1][c] != "#":
			next_pos.add((r+1, c))

	return list(next_pos.difference(visited))

# main code

# read all the lines
with open('Challenges/ch23/input.txt') as f:
    lines = f.read().splitlines()

# global variables

map = lines
n_rows = len(map)
n_cols = len(map[0])
start_pos = (1, 1) #note: instead of (0,1) we're going for the position after a first move, we'll just have to add+1 to the final result
map[0] = "#" * n_rows # forcing a forrest in the original starting position so that it can't go north from (1,1)

final_pos = (n_rows-1, n_cols-2)

# process data

## part 1
start_time = time.time()
result = 0



paths = []

paths_tree = deque()
paths_tree.append((start_pos, {start_pos})) # set((...)) syntax doesn't work / creates a normal set (!)
max_length = 0

while len(paths_tree) > 0:
	head = paths_tree.popleft()
	next_steps = next_positions(map, head[0], head[1])

	for next_step in next_steps:
		# check if we got to the final position
		if next_step == final_pos:
			print(f"Got to a final position in {len(head[1])+1} steps") # +1 to accomodate the step into the final position
			max_length = max(max_length, len(head[1])+1)
			# print_map(map, head[1])
		else:
			# print("##", next_step, head[1])		

			set_with_step = head[1].copy()
			set_with_step.add(next_step)
			paths_tree.append((next_step, set_with_step))

	# print(next_steps)


result = max_length
print(f"Result part 1: {result}")
print("--- %s seconds ---" % (time.time() - start_time))

# part 1: 2018 in 3.6 seconds

## part 2

# input("*********** Press Enter to continue... **********")
# start_time = time.time()
# print("Result part 2: ", result) #
# print("--- %s seconds ---" % (time.time() - start_time))

