import sys
import numpy as np
from collections import Counter
import re
import copy
from tqdm import tqdm
import time
from collections import deque
import random

# functions
def print_as_map(map, pos):

    for r in range(0, nrows):
        for c in range(0, ncols):

            if [r, c] in pos:
                print("x", end="")
            else:
                print(map[r][c], end="")
        print()

def calculate_possible_moves(map):
    next_positions = { } # hash table: position -> list of next positions

    for row_index in range(0, nrows):
        for col_index in range(0, ncols):
            ht_key = (row_index, col_index)

            # calculate available next positions
            if map[row_index][col_index] == "#":
                continue

            next_positions[ht_key] = []

            # left
            if col_index>0 and map[row_index][col_index-1] == ".":
                next_positions[ht_key].append((row_index, col_index-1))

            # right
            if col_index<ncols-1 and map[row_index][col_index+1] == ".":
                next_positions[ht_key].append((row_index, col_index+1))

            # up
            if row_index>0 and map[row_index-1][col_index] == ".":
                next_positions[ht_key].append((row_index-1, col_index))

            # down
            if row_index<nrows-1 and map[row_index+1][col_index] == ".":
                next_positions[ht_key].append((row_index+1, col_index))

            # print(next_positions[ht_key])

    return next_positions


# main code

# read all the lines
with open('Challenges/ch21/input.txt') as f:
    lines = f.read().splitlines()

map = lines

# find position of S
for rowIdx, row in enumerate(map):
    pos = row.find("S")

    if pos != -1:
        break

sPos = (rowIdx, pos) # tuple

map[rowIdx] = map[rowIdx].replace("S", ".") # to treat it as a normal plot and not having to treat it specially

nrows = len(map)
ncols = len(map[0])




# global variables
result = 0
next_positions_ht = calculate_possible_moves(map)

# process data

# part 1
start_time = time.time()

positions_to_explore_queue = deque()
positions_to_explore_queue.append(sPos)
pos_after_step = set()

for nstep in range(0, 64):

    pos_after_step.clear()

    while len(positions_to_explore_queue) > 0:
        pos = positions_to_explore_queue.popleft()

        ht_key = pos

        [pos_after_step.add(p) for p in next_positions_ht[ht_key]]
    
    # now that we have finished exploring the step, we add everything that is in the set into the queue
    for pas in pos_after_step:
        positions_to_explore_queue.append(pas)
    
    # print(pos_after_step)
    print(f"Size of queue {len(positions_to_explore_queue)}")




# print_as_map(map, positions_to_explore_queue)

print("Result part 1: ", len(positions_to_explore_queue))
print("--- %s seconds ---" % (time.time() - start_time))

# part 2



# input("*********** Press Enter to continue... **********")
# start_time = time.time()
# print("Result part 2: ", result) #
# print("--- %s seconds ---" % (time.time() - start_time))

