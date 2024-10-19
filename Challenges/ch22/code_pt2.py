import time
from collections import deque
import sys
import numpy as np
from collections import Counter
import re
import copy
from tqdm import tqdm
import random

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

def count_possible_drops(blocks, index_to_skip):
    """Count how many blocks were dropped by removing a block in a given position, which is ignored in the processing"""
    """Note that the drop may be of more than one position, so this has to replicate the logic of the original drop code"""

    cubes = set()

    current_index = -1
    count_drops = 0

    while len(blocks) > 0:
        current_index += 1
        head, blocks = blocks[0], blocks[1:]

        if index_to_skip == current_index:
            continue

        # we're at the bottom already
        if head[0][2] == 0:
            cubes = cubes.union(break_block_to_cubes(head))
            continue

        #else let's try and drop one
        dropped = False
        while True:
                drop_one = ((head[0][0], head[0][1], head[0][2]-1), (head[1][0], head[1][1], head[1][2]-1))

                if len(cubes.intersection(break_block_to_cubes(drop_one))) > 0:
                    # we had the position of the previous position before the drop
                    cubes = cubes.union(break_block_to_cubes(head))
                    break
                elif drop_one[0][2] == 0:
                    # we just got to the bottom / found the final position

                    dropped = True
                    cubes = cubes.union(break_block_to_cubes(drop_one))
                    break
                else:
                    head = drop_one
                    dropped = True
        
        if dropped == True:
            count_drops += 1

    return count_drops

break_block_cache = dict()
def break_block_to_cubes(block):
    """Decompose a 'tetris piece' in its component cubes and return the respective tuples in a set"""
    """Using the ht yields a 3 second improvement of the 24 total to 21"""

    if block in break_block_cache:
        return break_block_cache[block]

    broken_block = set()
    for x in range(block[0][0], block[1][0] +1):
        for y in range(block[0][1], block[1][1] +1):
            for z in range(block[0][2], block[1][2] +1):
                broken_block.add( (x,y,z))
 
    break_block_cache[block] = broken_block
    return broken_block


## Initial drop code -- let's drop all the bricks to the bottom
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


## 03. Now that we've dropped the pieces, let's remove one of the blocks/bricks of the collection one at a time, and see if we can drop without it
# let's sort again, which will allow us to optimize the drop check
processed.sort(key=lambda tup: tup[0][2])  # sorts in place

result = 0
for j in tqdm(range(0, len(processed))):
    result += count_possible_drops(processed, j)
    # print(f"After removing brick {j}, result = {result}")


print(f"Result part 2: {result}")
print("--- %s seconds ---" % (time.time() - start_time))

# right result is 109531 in 36 seconds