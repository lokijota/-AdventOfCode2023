import numpy as np
from collections import Counter
import re
import copy

# functions

# generate north / east / west / south positions -- there are no diagonals
# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
def generateSuroundingPositions(pipe, row, col):
    # print("generate for: ", pipe)
    global map
    surroundingPos = []

    if pipe == "S":
        if map[row-1][col] in ["|", "7", "F"]:
            surroundingPos.append([row-1, col])
        
        if map[row][col-1] in ["-", "L", "F"]:
            surroundingPos.append([row, col-1])

        if map[row][col+1] in ["-", "J", "7"]:
            surroundingPos.append([row, col+1])

        if map[row+1][col] in ["|", "L", "J"]:
            surroundingPos.append([row+1, col])

    else:
        if pipe in ["|", "L", "J"]: # north
            surroundingPos.append([row-1, col])

        if pipe in ["-", "J", "7"]: # west
            surroundingPos.append([row, col-1])
        
        if pipe in ["-", "L", "F"]: # east
            surroundingPos.append([row, col+1])
        
        if pipe in ["|", "7", "F"]: # south
            surroundingPos.append([row+1, col])


    return surroundingPos


# main code

# read all the lines
with open('input.txt') as f:
    lines = f.read().splitlines()

# add padding to make it simpler to process / no need to test edges
emptyRow = '.' * len(lines[0])
lines.append(emptyRow)
lines.insert(0, emptyRow)

map = []
for line in lines:
    map.append('.' + line + '.')

# global variables

# parse data into data structures

# find position of S
for rowIdx, row in enumerate(map):
    pos = row.find("S")

    if pos != -1:
        break

sPos = [rowIdx, pos]

visited = []
paths = [[sPos]]

# first round of paths
# suroundingPositions = generateSuroundingPositions('S', sPos[0], sPos[1])
# for sp in suroundingPositions:
#     path = [sPos]
#     path.append(sp)
#     paths.append(path)

print(paths)
# [[[36, 18], [35, 18]], [[36, 18], [36, 17]], [[36, 18], [36, 19]], [[36, 18], [37, 18]]]

newPaths = []
loopSize = 0
while True:
    for path in paths:
        # print()
        # print("********** Processing path: ", path)
        suroundingPositions = generateSuroundingPositions(map[path[-1][0]][path[-1][1]], path[-1][0], path[-1][1])

        # print(" ** Surrounding:", suroundingPositions)
        filteredSp = []
        for sp in suroundingPositions:
            if sp == sPos and len(path) > 2:
                # we found the loop
                loop = len(path)
                # print("LOOP: ", loop) -- finds it twice
            else:
                if sp not in path:
                    filteredSp.append(sp)
                # else:
                #     print(sp, " is in path, so not adding")

        for fsp in filteredSp:
            np = path.copy() # isto é desnecessário
            np.append(fsp)
            # print(" np", np)
            newPaths.append(np)
        
    # print(".", end="")
    # print("New paths, out of loop: ", newPaths)
    paths = newPaths
    newPaths = []

    if len(paths) == 0:
        break
    elif len(paths) == 2:
        paths=[paths[0]]

    # print(len(paths[0]), " / ", end="", flush=True)

result = int(loop/2)
print()
print("Half of loop: ", result)

# part 1 - 6897

# Nota: só há um loop. por isso na verdade só precisamos de gerar uma direcção, quando saímos do S... 
# da mesma forma n precisamos de fazer um deep copy. e tb n precisamos de comparar com a lista toda mas só com o final