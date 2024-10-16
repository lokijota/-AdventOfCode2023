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

def break_block_to_cubes(block):
    broken_block = set()

    for x in range(block[0][0], block[1][0] +1):
        for y in range(block[0][1], block[1][1] +1):
            for z in range(block[0][2], block[1][2] +1):
                broken_block.add( (x,y,z))
 
    return broken_block
    

highest_peak = 1

print(blocks)
print("---")
while len(blocks) > 0:
    head, blocks = blocks[0], blocks[1:]
    print(f"processing head: {head}")

    landed = False

    while landed == False:

        if head[0][2] == 1:
            print(" ---- reached height 1")
            landed = True
            highest_peak = head[1][2]
            cubes = cubes.union(break_block_to_cubes(head))
            processed.append(head)
            break
        
        height_to_drop = head[0][2] - highest_peak - 1
        safe_drop = ((head[0][0],head[0][1],head[0][2]-height_to_drop),(head[1][0],head[1][1],head[1][2]-height_to_drop))
        print(f" ---- safe dropped to {safe_drop}")

        # now drop one by one
        while True:
            next_drop = ((safe_drop[0][0], safe_drop[0][1], safe_drop[0][2]-1), (safe_drop[1][0], safe_drop[1][1], safe_drop[1][2]-1))
            next_drop_cubes = break_block_to_cubes(next_drop)

            if len(cubes.intersection(next_drop_cubes)) > 0: # landed, we use the last safe_drop value as the final position
                print(f" ---- landed at {next_drop}")

                landed = True
                processed.append(safe_drop)
                cubes = cubes.union(break_block_to_cubes(safe_drop))
                highest_peak = safe_drop[1][2]
                break
            elif next_drop[0][2] == 1: # if there is no intersection but we've reached the botton of z
                print(f" ---- reached bottom")

                landed = True
                processed.append(next_drop)
                cubes = cubes.union(break_block_to_cubes(next_drop))
                highest_peak = next_drop[1][2]
                break
            else:
                print(f" ---- dropping one more")

                safe_drop = next_drop # keep dropping


# print(processed)


# ---- se eu conseguir construir um grafo do que está assente em quê sem ter de os fazer cair, era o ideal!


print(f"Result part 1: {result}")
print("--- %s seconds ---" % (time.time() - start_time))

# part 2


# for r in range(0,8):
#     print(f"Area of {r} is", calculate_area_losange(r))



# input("*********** Press Enter to continue... **********")
# start_time = time.time()
# print("Result part 2: ", result) #
# print("--- %s seconds ---" % (time.time() - start_time))

