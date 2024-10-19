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
with open('Challenges/ch22/input.txt') as f:
    lines = f.read().splitlines()

blocks = []

for line in lines:
    result = re.search("(\d+),(\d+),(\d+)\~(\d+),(\d+),(\d+)", line)
    start = (int(result.group(1)), int(result.group(2)), int(result.group(3))) 
    end = (int(result.group(4)), int(result.group(5)), int(result.group(6))) 
    blocks.append((start, end))

# print the size of each block in cubes and the total number of cubes 
# sum=0
# for block in blocks:
#     size = abs(block[1][0] - block[0][0]) + \
#            abs(block[1][1] - block[0][1]) + \
#            abs(block[1][2] - block[0][2])
#     size += 1
#     print(block[0], "-", block[1], "size=", size)

#     sum += size

# print(f"Total:", sum)

# global variables

# process data

# part 1
start_time = time.time()
result = 0

## 01. sort the blocks by start-z
blocks.sort(key=lambda tup: tup[0][2])  # sorts in place

processed = []
cubes = set()

## 02. start with the block with lowest z-start / if z-start = 1 it's in final position, thus move to the processed list and break down the cubes

def check_drop_possible(blocks):
    """Check if it's possible to drop at least one position. Note that z is 0-based, not 1-based as in AOC challenge page"""

    cubes = set()

    while len(blocks) > 0:
        head, blocks = blocks[0], blocks[1:]

        # we're at the bottom already
        if head[0][2] == 0:
            cubes = cubes.union(break_block_to_cubes(head))
            continue

        #else let's try and drop one
        drop_one = ((head[0][0], head[0][1], head[0][2]-1), (head[1][0], head[1][1], head[1][2]-1))

        if len(cubes.intersection(break_block_to_cubes(drop_one))) > 0:
            # can't drop one, it's overlapping a block below
            cubes = cubes.union(break_block_to_cubes(head))
            continue

        # we were able to drop at least 1 position, so return True, i.e., block we're processing can't be disintegrated
        return True

    return False

def break_block_to_cubes(block):
    """Decompose a 'tetris piece' in its component cubes and return the respective tuples in a set"""

    broken_block = set()

    for x in range(block[0][0], block[1][0] +1):
        for y in range(block[0][1], block[1][1] +1):
            for z in range(block[0][2], block[1][2] +1):
                broken_block.add( (x,y,z))
 
    return broken_block

def generate_plot(blocks):
    """Used this to debug by printing a visual representation of the cube. As it is, it prints all blocks in grey except the last one in colour"""
    """It's easy to change to alternate colours each time it prints a block"""
    # find space of blocks
    max_x = 0
    max_y = 0
    max_z = 0

    for block in blocks:
        if block[1][0] > max_x:
            max_x = block[1][0]

        if block[1][1] > max_y:
            max_y = block[1][1]

        if block[1][2] > max_z:
            max_z = block[1][2]
    
    max_x += 1
    max_y += 1
    max_z += 1

    # now prepare the voxels
    n_voxels = np.zeros((max_x, max_y, max_z), dtype=bool)
    # set the colors of each object
    colors = np.empty(n_voxels.shape, dtype=object)

    current_colour = 'red'
    for block in blocks:
        cubes = break_block_to_cubes(block)

        for cube in cubes:
            n_voxels[cube] = True
            colors[cube] = 'grey' # current_colour

        # if current_colour == 'red':
        #     current_colour = 'blue'
        # elif current_colour == 'blue':
        #     current_colour = 'green'
        # elif current_colour == 'green':
        #     current_colour = 'yellow'
        # else:
        #     current_colour = 'red'


    # paint last block in a different colour
    last_block = blocks[-1]
    print(f"##### Printing block {last_block}")
    cubes = break_block_to_cubes(last_block)

    for cube in cubes:
        n_voxels[cube] = True
        colors[cube] = 'red' # current_colour
    
    # and plot everything
    ax = plt.figure().add_subplot(projection='3d')
    ax.voxels(n_voxels, facecolors=colors, edgecolor='k')

    # plt.savefig('blocks.png', bbox_inches='tight')
    plt.show()
    
    return


highest_peak = 0

while len(blocks) > 0:
    head, blocks = blocks[0], blocks[1:]
    # print(f"processing next highest block: {head}")

    landed = False

    while landed == False:

        # note: to avoid special processing (&repeated code) of the blocks already at z=1, assume bottom is at z=0 / so that blocks always actually drop by +1 position

        # we can safely drop by N positions to the previous highest block. For blocks on (x,y,1) doesn't actually drop anything
        height_to_drop = head[0][2] - highest_peak - 1
        safe_drop = ((head[0][0],head[0][1],head[0][2]-height_to_drop),(head[1][0],head[1][1],head[1][2]-height_to_drop))
        # print(f" ---- safe dropped to {safe_drop}, highest_peak = {highest_peak}")

        # now drop one by one
        while True:
            next_drop = ((safe_drop[0][0], safe_drop[0][1], safe_drop[0][2]-1), (safe_drop[1][0], safe_drop[1][1], safe_drop[1][2]-1))
            next_drop_cubes = break_block_to_cubes(next_drop)

            if len(cubes.intersection(next_drop_cubes)) > 0: # landed in prev position, it's over some block before dropping one down / we use the last safe_drop value as the final position
                # print(f" ---- landed at {safe_drop}")

                landed = True
                processed.append(safe_drop)
                cubes = cubes.union(break_block_to_cubes(safe_drop))
                
                if safe_drop[1][2] > highest_peak:
                    highest_peak = safe_drop[1][2]
                break
            elif next_drop[0][2] == 0: # if there is no intersection but we've reached the botton of z
                # print(f" ---- reached bottom at {next_drop}")

                landed = True
                processed.append(next_drop)
                cubes = cubes.union(break_block_to_cubes(next_drop))
                if next_drop[1][2] > highest_peak:
                    highest_peak = next_drop[1][2]
                break
            else:
                # print(f" ---- dropping one more")

                safe_drop = next_drop # keep dropping

        # piece by piece drop
        # generate_plot(processed)

# print(processed)
# generate_plot(processed)

## 03. Now that we've dropped the pieces, let's remove one of the blocks/bricks of the collection one at a time, and see if we can drop without it

result = 0
for j in tqdm(range(0, len(processed))):

    # note: I'm sure this could be more efficient

    removed_block = processed.pop(j) # O(n) complexity
    if not check_drop_possible(processed):
        result += 1
        # print(f"Block {j} can be disintegrated (doesn't causes drops)")
    # else:
    #     print(f"Block {j} can't be disintegrated (causes drops)")
    
    processed.insert(j, removed_block) # O(n) complexity

print(f"Result part 1: {result}")
print("--- %s seconds ---" % (time.time() - start_time))

# first submission was 702 -- too high
# right submission is 519, takes 24 secs

# part 2




# input("*********** Press Enter to continue... **********")
# start_time = time.time()
# print("Result part 2: ", result) #
# print("--- %s seconds ---" % (time.time() - start_time))

