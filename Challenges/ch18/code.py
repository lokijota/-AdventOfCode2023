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
def calculateBoundaries(instructions):
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

    return boundaries

boundaries = calculateBoundaries(instructions)
print("Boundaries: ", boundaries)

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

start_time = time.time()

result = -1

newInstructions = []

for instruction in instructions:
    hex = int("0x" + instruction[2][1:6], 16)
    dir = instruction[2][6]
    match dir:
        case "0":
            dir = "R"
        case "1":
            dir = "D"
        case "2":
            dir = "L"
        case "3":
            dir = "U"

    newInstructions.append([dir,hex])    

print(calculateBoundaries(newInstructions))
# print(newInstructions)

# convert instructions to pixel locations

# debug_sample = [ \
#     ['R', 6],\
#     ['D', 5],\
#     ['L', 2], \
#     ['D', 2],\
#     ['R', 2], \
#     ['D', 2], \
#     ['L', 5], \
#     ['U', 2], \
#     ['L', 1], \
#     ['U', 2], \
#     ['R', 2], \
#     ['U', 3], \
#     ['L', 2],\
#     ['U', 2]\
# ]

# newInstructions = debug_sample
# print(newInstructions)

current_loc = [0,0]
px_locations = []
px_locations.append(current_loc.copy())

# let's use (x,y) instead of (r,c)
edge_size = 0
for instruction in newInstructions:
    if instruction[0] == "R":
        current_loc[0] += instruction[1]
        
    elif instruction[0] == "L":
        current_loc[0] -= instruction[1]

    elif instruction[0] == "U":
        current_loc[1] += instruction[1]
    else:
        current_loc[1] -= instruction[1]

    edge_size += instruction[1]
    px_locations.append([current_loc[0], current_loc[1]])

# print(px_locations)

px_locations.reverse()

# shoelace algorithm
    
sum = 0
for j in range(0, len(px_locations)-1):
    sum += px_locations[j][0] * px_locations[j+1][1]
    sum -= px_locations[j][1] * px_locations[j+1][0]

result = int(sum/2)
result += int(edge_size/2+1) # this is specific for pixel solutions... need to add the boundary/2 + 1, as it's pixelated not an area

print("Result part 2: ", result) 
print("--- %s seconds ---" % (time.time() - start_time))

# 39544385834783 is too low
# 79088771669566 is too low
# 79088855654037