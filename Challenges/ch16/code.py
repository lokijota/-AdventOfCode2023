import numpy as np
from collections import Counter
import re
import copy
from tqdm import tqdm
import time
from collections import deque

# functions

# main code

# read all the lines
with open('Challenges/ch16/input.txt') as f:
    lines = f.read().splitlines()

# parse data file content

nrows = len(lines)
ncols = len(lines[0])
activations = np.zeros( (nrows, ncols), dtype=int)
map = lines

# print(activations)

# global variables

beamheads = deque() # remember: LIFO
beamheads.append([0, 0, "E"]) # or appendLeft()

bitFlag = {}
bitFlag["N"] = 0b1000
bitFlag["S"] = 0b0100
bitFlag["E"] = 0b0010
bitFlag["W"] = 0b0001

# functions

def beamMove(map, beamhead):

    r = beamhead[0]
    c = beamhead[1]
    direction = beamhead[2]

    # we always get valid positions when we get here
    mapElement = map[r][c]

    if mapElement == ".":
        match direction:
            case "E":
                return[[r,c+1,direction]]
            case "S":
                return[[r+1,c,direction]]
            case "N":
                return[[r-1,c,direction]]
            case "W":
                return[[r,c-1,direction]]
            
    if mapElement == "-":
        match direction:
            case "E":
                return [[r,c+1,direction]]
            case "S":
                return [[r,c-1,"W"],[r,c+1,"E"]]
            case "N":
                return [[r,c-1,"W"],[r,c+1,"E"]]
            case "W":
                return [[r,c-1,direction]]
        
    if mapElement == "|":
        match direction:
            case "E":
                return [[r-1,c,"N"],[r+1,c,"S"]]
            case "S":
                return [[r+1,c,direction]]
            case "N":
                return [[r-1,c,direction]]
            case "W":
                return [[r-1,c,"N"],[r+1,c,"S"]]

    if mapElement == "\\":
        match direction:
            case "E":
                return[[r+1,c,"S"]]
            case "S":
                return[[r,c+1,"E"]]
            case "N":
                return[[r,c-1,"W"]]
            case "W":
                return[[r-1,c,"N"]]
    
    if mapElement == "/":
        match direction:
            case "E":
                return[[r-1,c,"N"]]
            case "S":
                return[[r,c-1,"W"]]
            case "N":
                return[[r,c+1,"E"]]
            case "W":
                return[[r+1,c,"S"]]

    print("beamMove() - I SHOULD NOT HAVE GOTTEN HERE, mapElement=", mapElement)
    return []

# process data

start_time = time.time()

while len(beamheads) > 0:

    beamhead = beamheads.pop()
    if beamhead[0] >= 0 and beamhead[0] < nrows and beamhead[1] >= 0 and beamhead[1] < ncols:
            
            # get bit indicated by positinn binN
            currentIndicator = activations[beamhead[0]][beamhead[1]] & bitFlag[beamhead[2]]
            if currentIndicator == 0:
                activations[beamhead[0]][beamhead[1]] |= bitFlag[beamhead[2]]
            
                # print(activations)

                nextbeams = beamMove(map, beamhead)

                # print(str(beamheads))
                # input("PAK" + str(nextbeams) + ":")

                for nextbeam in nextbeams:
                    beamheads.append(nextbeam)

# print(activations)

result = np.count_nonzero(activations)

print("Result part 1: ", result) # part 1 - 6906

print("--- %s seconds ---" % (time.time() - start_time))

# part 2

result = 0

print("Result part 2: ", result)
