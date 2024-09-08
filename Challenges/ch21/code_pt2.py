import sys
import numpy as np
from collections import Counter
import re
import copy
from tqdm import tqdm
import time
from collections import deque
import random
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


# functions
def print_as_map(map, pos):

    for r in range(0, nrows):
        for c in range(0, ncols):

            if (r, c) in pos:
                print("O", end="")
            else:
                print(map[r][c], end="")
        print()


def print_as_map_inner_rocks_replace(map, pos, ray, center):

    count_inner_stones = 0
    for r in range(0, nrows):
        for c in range(0, ncols):

            if (r, c) in pos:
                print("O", end="")
            else:

                # this is wrong as the distance to the center is wrong: this is not a circumference
                if map[r][c] == "#":
                    
                    point = Point(c, r)
                    polygon = Polygon([(0, ray), (ray, 0), (ray*2, ray), (ray, ray*2)])
                    # print(polygon.contains(point))

                    if polygon.contains(point):
                        print("@", end="")
                        count_inner_stones += 1
                    else:
                        print(map[r][c], end="")

                else:
                    print(map[r][c], end="")
        print()

    return count_inner_stones

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

def calculate_area_losange(ray):
    return ray**2 + (ray-1)**2

def calculate_area_of_O(ray):
    # calculating the area of a losang where it's O.O.O.O.O alternating, is the same as the area of the square
    # which is super convenient and simple
    # other way would be to do calculate_area_losange(ray) - calculate_area_square(ray-1), which would yeld the same result
    return ray**2

def count_rocks_overlaying_reached_garden_plots():

    return 0


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

inner_stones = print_as_map_inner_rocks_replace(map, positions_to_explore_queue, 64, (64,64))

print(f"Area of 64 is", calculate_area_of_O(64))
print(f"Stones inside", inner_stones)
print("delta:", calculate_area_of_O(64) - inner_stones)
# isto n está certo. preciso de contar apenas os # que estejam overlapping com 0...


# for r in range(0,8):
#     print(f"Area of {r} is", calculate_area_losange(r))



# input("*********** Press Enter to continue... **********")
# start_time = time.time()
# print("Result part 2: ", result) #
# print("--- %s seconds ---" % (time.time() - start_time))

