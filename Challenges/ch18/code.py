import numpy as np
from collections import Counter
import re
import copy
from tqdm import tqdm
import time
from collections import deque
import random

# functions

# main code

# read all the lines
with open('Challenges/ch18/input.txt') as f:
    lines = f.read().splitlines()

# parse data file content
instructions = []
for line in lines:
    # R 6 (#70c710)
    parts = line.split(" ")

    rgb = parts[2].replace("(", "").replace(")", "")
    instructions.append( [parts[0], int(parts[1]), rgb])

# print(instructions)

# find boundaries
boundaries = [0,0,0,0] # top left / bottom right, row-column
current = [0,0]

for instruction in instructions:
    if instruction[0] == "R":
        current[1] += instruction[1]
        if current[1] > boundaries[3]:
            boundaries[3] = current[1]

    elif instruction[0] == "L":
        current[1] -= instruction[1]
        if current[1] < boundaries[1]:
            boundaries[1] = current[1]

    elif instruction[0] == "D":
        current[0] += instruction[1]
        if current[0] > boundaries[2]:
            boundaries[2] = current[0]
            
    elif instruction[0] == "U":
        current[0] -= instruction[1]
        if current[0] < boundaries[0]:
            boundaries[0] = current[0]

print(boundaries)

nrows = boundaries[2] - boundaries[0]
ncols = boundaries[3] - boundaries[1]
startPos = [ 0 - boundaries[0], 0 - boundaries[1]]
print("size: ", nrows, ncols)
print("start pos: ", startPos)

# global variables
map = np.zeros((nrows+1,ncols+1), dtype=int)

# functions

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printMap(map):
    for r in range(0, nrows+1):
        for c in range(0, ncols+1):

            if map[r][c] == 1:
                print(f"{bcolors.OKGREEN}#{bcolors.ENDC}", end="")
            else:
                print(".", end="")
        print()

# process data

map[startPos[0]][startPos[1]] = 1
for instruction in instructions:

    for j in range(1, instruction[1]+1):
        if instruction[0] == "R":
            startPos[1] += 1
        elif instruction[0] == "L":
            startPos[1] -= 1
        elif instruction[0] == "D":
            startPos[0] += 1
        elif instruction[0] == "U":
            startPos[0] -= 1

        map[startPos[0]][startPos[1]] = 1

def generateSurroundingPositions(pos):
    surroundingPositions = []

    if pos[1] > 0:
        surroundingPositions.append([pos[0], pos[1]-1])

    if pos[0] > 0:
        surroundingPositions.append([pos[0]-1, pos[1]])
    
    if pos[1]+1 < ncols:
        surroundingPositions.append([pos[0], pos[1]+1])

    if pos[0]+1 < nrows:
        surroundingPositions.append([pos[0]+1, pos[1]])

    return surroundingPositions

def fill(map):
    # find an interior pixel
    c = 0
    while map[1][c] == 0:
        c += 1
    c+=1

    # flood fill
    positions = generateSurroundingPositions([1,c])
    while positions:
        pos = positions.pop()
        if map[pos[0]][pos[1]] == 0:
            map[pos[0]][pos[1]] = 1
            positions += generateSurroundingPositions(pos)

# part 1
fill(map)
# printMap(map)
result = map.sum()
# printMap(map)


start_time = time.time()

print("Result part 1: ", result) # part 1 - 
print("--- %s seconds ---" % (time.time() - start_time))

# 3662 is too low
# 67110 is too high
# 56678 is the right answer

# part 2

result = -1

start_time = time.time()
print("Result part 2: ", result) 
print("--- %s seconds ---" % (time.time() - start_time))
