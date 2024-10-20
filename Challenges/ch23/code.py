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

next_positions_cache = dict()
def next_positions(map, pos, visited, with_slopes = True):
	next_pos = set() 
	r = pos[0]
	c = pos[1]

	if pos in next_positions_cache:
		return next_positions_cache[pos].difference(visited)

	# ugly urgh but that else: means it's this or 4 and's with_slopes per execution
	if with_slopes:
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
	else:
		if map[r][c+1] != "#":
			next_pos.add((r, c+1))

		if map[r][c-1] != "#":
			next_pos.add((r, c-1))

		if map[r-1][c] != "#":
			next_pos.add((r-1, c))

		if map[r+1][c] != "#":
			next_pos.add((r+1, c))

	next_positions_cache[pos] = next_pos

	return next_pos.difference(visited) # list () removed from previous commit / 1/3 speed up on part 1

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

paths_tree = deque()
paths_tree.append((start_pos, {start_pos})) # set((...)) syntax doesn't work / creates a normal set (!)
max_length = 0

while len(paths_tree) > 0:
	head = paths_tree.pop() # previous version had popleft which was actually a breadth-first!
	next_steps = next_positions(map, head[0], head[1], False) # True -- part 1 / False -- part 2

	for next_step in next_steps:
		# check if we got to the final position
		if next_step == final_pos:
			max_length = max(max_length, len(head[1])+1)
			print(f"Got to a final position in {len(head[1])+1} steps, max = {max_length}") # +1 to accomodate the step into the final position
			# print_map(map, head[1])
		else:
			# print("##", next_step, head[1])		

			# optimization as several times we're in a corridor with only one way
			if len(next_steps) > 1:
				set_with_step = head[1].copy() # this is probably the slowest part of this code
			else:
				set_with_step = head[1]

			set_with_step.add(next_step)
			paths_tree.append((next_step, set_with_step))

	# print(next_steps)


result = max_length
print(f"Result part 1: {result}")
print("--- %s seconds ---" % (time.time() - start_time))

# part 1: 2018 in 1.1 seconds

## part 2

# Result part 2: 6406
# --- 10420.81382393837 seconds ---
# could be optimized a lot more with a graph and eliminating the "corridors" (linear paths through the map)

# input("*********** Press Enter to continue... **********")
# start_time = time.time()
# print("Result part 2: ", result) #
# print("--- %s seconds ---" % (time.time() - start_time))

