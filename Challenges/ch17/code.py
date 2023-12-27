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
with open('Challenges/ch17/input.txt') as f:
    lines = f.read().splitlines()

# parse data file content

nrows = len(lines)
ncols = len(lines[0])
map = lines

# global variables

# weight of a given path, nodes it's been through
# paths = [ [int(map[0][0]) , [[0,0]]] ]
paths = [ [0 , [[0,0]]] ] # start with weight 0, as first square doesn't count

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

def printPath(map, path):

    for r in range(0, nrows):
        for c in range(0, ncols):

            if [r,c] in path:
                print(f"{bcolors.OKGREEN}{map[r][c]}{bcolors.ENDC}", end="")
            else:
                print(map[r][c], end="")
        print()



# map is the matrix, path is for example: [map[0][0] , [(0,0), (1,0) ]] 
def generateSurroundingPositions(map, pos):
    surroundingPositions = []

    # order is relevant. what I put in the end is explored first.

    if pos[1] > 0 and pos[0] != nrows-1:
        surroundingPositions.append([pos[0], pos[1]-1])

    if pos[0] > 0 and pos[1] != ncols-1:
        surroundingPositions.append([pos[0]-1, pos[1]])
    
    if pos[1]+1 < ncols:
        surroundingPositions.append([pos[0], pos[1]+1])

    if pos[0]+1 < nrows:
        surroundingPositions.append([pos[0]+1, pos[1]])


    # um: 2480 / secs: 357.76004004478455
    return surroundingPositions

# vertical or horizontal
def filterOutInvalidPositions(path, surroundingPositionsList):
    validPosition = []

    # remove positions that are already in the path
    unvisitedPositions = [pos for pos in surroundingPositionsList if pos not in path[1]]

    if len(path[1]) >= 4:

        # all in same row or column
        last3 = path[1][-4:]

        for sp in unvisitedPositions:
                if (last3[0][0] == last3[1][0] and last3[1][0] == last3[2][0] and last3[2][0] == last3[3][0] and last3[3][0] == sp[0]) or \
                (last3[0][1] == last3[1][1] and last3[1][1] == last3[2][1] and last3[2][1] == last3[3][1] and last3[3][1] ==sp[1]):
                    continue

                validPosition.append(sp)

        return validPosition

    else:
        return unvisitedPositions
    
    
def generateNextMovements(map, path):
    nextPositions = generateSurroundingPositions(map, path[1][-1])
    nextPositions = filterOutInvalidPositions(path, nextPositions)
    return nextPositions

def findShortestPath(map, paths):
    global start_time

    min = 1545 # Found new mininum: 2002 / secs: 26876.768674135208 len(paths):  473 len(path): 414
               # Found new mininum: 1573 / secs: 5.826629877090454 len(paths):  410 len(path): 320

    while paths: # if not empty

        # if random.random() > 0.8:
        #     nextitem = random.randint(int((len(paths)-1)/2), len(paths)-1)
        #     path = paths[nextitem]

        #     if nextitem+1 < len(paths):
        #         paths = paths[:nextitem] + paths[nextitem+1:]
        #     else:
        #         paths = paths[:nextitem]
        # else:            
        path = paths[0]
        paths = paths[1:]

        nextMovements = generateNextMovements(map, path)

        # update weight and add to the list
        for nextMovement in nextMovements:

            if int(map[nextMovement[0]][nextMovement[1]]) >= 8 or len(path[1]) > 316:
                continue

            # skip paths that are doomed
            manhattanDistanceToEnd = nrows - nextMovement[0] -1 + ncols - nextMovement[1] -1
            if path[0] + int(map[nextMovement[0]][nextMovement[1]]) + manhattanDistanceToEnd*3 > min:
                continue

            # printPath(map, path[1])
            # input()
            
            cloneList = [path[0] + int(map[nextMovement[0]][nextMovement[1]])]
            cloneList = cloneList + [path[1] + [nextMovement]]

            # we got to the end
            if nextMovement[0] == nrows-1 and nextMovement[1] == ncols-1:
                if cloneList[0] < min:
                    min = cloneList[0]
                    print("Found new mininum:", min, "/ secs:", (time.time() - start_time), "len(paths): ", len(paths), "len(path):", len(path[1]))
                    printPath(map, cloneList[1])
                    # print(path)
                else:
                    print(".")
            else:
                paths = [cloneList] + paths

    return min

# process data

# part 1

result = 0

start_time = time.time()

result = findShortestPath(map, paths)

print("Result part 1: ", result) # part 1 - 6906
print("--- %s seconds ---" % (time.time() - start_time))

# 2419 is too high /  Found new mininum: 2419 / secs: 37212.687748909
# 1559 is too high Found new mininum: 1559 / secs: 157.61041522026062 len(paths):  405 len(path): 318


# part 2

result = -1

start_time = time.time()
print("Result part 2: ", result) 
print("--- %s seconds ---" % (time.time() - start_time))
