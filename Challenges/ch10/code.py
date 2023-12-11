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
finalPath = None
while True:
    for path in paths:
        # print()
        # print("********** Processing path: ", path)
        suroundingPositions = generateSuroundingPositions(map[path[-1][0]][path[-1][1]], path[-1][0], path[-1][1])

        # print(" ** Surrounding:", suroundingPositions)
        filteredSp = []
        for sp in suroundingPositions:
            if sp == sPos and len(path) > 2:
                # we found the loop!
                loop = len(path)
                finalPath = path.copy()
                break
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
    elif len(paths) == 2: # optimize, go only one direction
        paths=[paths[0]]

    # print(len(paths[0]), " / ", end="", flush=True)

result = int(loop/2)
print()
print("Half of loop: ", result)

# part 1 - 6897

# Nota: só há um loop. por isso na verdade só precisamos de gerar uma direcção, quando saímos do S... 
# da mesma forma n precisamos de fazer um deep copy. e tb n precisamos de comparar com a lista toda mas só com o final

######### part 2 #########

# functions

def findSymbol(prevPos, sPos, nextPos):

    # row above or below
    if abs(prevPos[0] - nextPos[0]) == 2:
        return "|"
    
    # column to the east or to the west
    if abs(prevPos[1] - nextPos[1]) == 2:
        return "-"
    
    # "diagonals"
    vector = [ nextPos[0]-prevPos[0], nextPos[1]-prevPos[1] ]
    
    if vector == [-1,1]:
        if sPos[0] < prevPos[0]:
            return "F"
        else:
            return "J"

    if vector == [1,1]:
        if sPos[0] > prevPos[0]:
            return "L"
        else:
            return "7"       

    if vector == [-1,-1]:
        if sPos[0] < prevPos[0]:
            return "7"
        else:
            return "L"
    
    if vector == [1,-1]:
        if sPos[0] > prevPos[0]:
            return "J"
        else:
            return "F"    

def findInnerPosition(pos, innerDirection):

    if innerDirection == "N":
        return [pos[0]-1, pos[1]]
    if innerDirection == "S":
        return [pos[0]+1, pos[1]]
    if innerDirection == "W":
        return [pos[0], pos[1]-1]
    if innerDirection == "E":
        return [pos[0], pos[1]+1]

def replaceCharAtStringPosition(fullString, index, character):
    return fullString[:index] + character + fullString[index+1:]

def rotateDirection(leftOrRight, direction):
    directionsClockwise = ["N", "E", "S", "W", "N"]
    
    if leftOrRight == "right":
        return directionsClockwise[directionsClockwise.index(direction)+1]
    else:
        directionsCounterClockwise = directionsClockwise.copy()
        directionsCounterClockwise.reverse()
        return directionsCounterClockwise[directionsCounterClockwise.index(direction)+1]
    
def floodFill(map, finalPath, innerPositions, startingPos):

    positionsToCheck = []
    positionsToCheck.append(startingPos)

    while len(positionsToCheck) > 0:

        pos = positionsToCheck[0]
    
        candidatePositions = []
        candidatePositions.append([pos[0]-1, pos[1]])
        candidatePositions.append([pos[0]+1, pos[1]])
        candidatePositions.append([pos[0], pos[1]-1])
        candidatePositions.append([pos[0], pos[1]+1])

        filteredPositions = []
        for cp in candidatePositions:
            if cp not in finalPath and cp[0] >= 0 and cp[0] < len(map) and cp[1] >= 0 and cp[1] < len(map[0]) \
                 and map[cp[0]][cp[1]] != "i" :  # no need to test innerPositions, as this is in sync with the map
                filteredPositions.append(cp)

        # update map and visited positions
        innerPositions += filteredPositions
        for fp in filteredPositions:
            map[fp[0]] = replaceCharAtStringPosition(map[fp[0]], fp[1], "i")
            # print("- Filled with i", fp)

        positionsToCheck += filteredPositions
        positionsToCheck = positionsToCheck[1:] # skip the first


    # these filtered positions are the next ones to visit


def printMap(map):
    for row in map:
        print(row)
    
# print(finalPath)

# 1. Replace S with the right character
s = findSymbol(finalPath[-1], finalPath[0], finalPath[1])

row = map[finalPath[0][0]]
startPart = row[:finalPath[0][1]]
endPart = row[finalPath[0][1]+1:]
map[finalPath[0][0]] = startPart + s + endPart
printMap(map)

# 2. Find a | or - on the path, keeping indication of the direction

startPosInPath = None


for startIndexInPath, pos in enumerate(finalPath):
    if map[pos[0]][pos[1]] == "|":
        startPosInPath = pos
        print("StartPosInPath: ", startPosInPath, " Symbol= |")
        break

    if map[pos[0]][pos[1]] == "-":
        startPosInPath = pos
        print("StartPosInPath: ", startPosInPath, " Symbol= -")
        break


# rebase the path so that it starts with the first positoin we're filling in
finalPath = finalPath[startIndexInPath:] + finalPath[:startIndexInPath]

# 3. Define a "inner direction" vector and start going over and updating to inner area

innerPositions = []
# prevSymbol = ""

innerDirection = ""
navigationDirection = ""

for pos in finalPath:

    currentSymbol = map[pos[0]][pos[1]]

    # if we're just starting
    if pos == finalPath[0]:
        if currentSymbol == "|":
            navigationDirection = "S"
            innerDirection = "W"
        elif currentSymbol == "-":
            navigationDirection = "E"
            innerDirection = "N"

    # we're not in the first position
    else:
        if navigationDirection == "N":
            if currentSymbol == "7":
                # turn left
                navigationDirection = "W"
                innerDirection = rotateDirection("left", innerDirection)
            elif currentSymbol == "F":
                # turn right
                navigationDirection = "E"
                innerDirection = rotateDirection("right", innerDirection)
            #elif currentSymbol == "|":
            # noop
        elif navigationDirection == "E":
            if currentSymbol == "7":
                # turn south
                navigationDirection = "S"
                innerDirection = rotateDirection("right", innerDirection)
            elif currentSymbol == "J":
                # turn right
                navigationDirection = "N"
                innerDirection = rotateDirection("left", innerDirection)

        elif navigationDirection == "S":
            if currentSymbol == "L":
                # turn right
                navigationDirection = "E"
                innerDirection = rotateDirection("left", innerDirection)
            elif currentSymbol == "J":
                # turn left
                navigationDirection = "W"
                innerDirection = rotateDirection("right", innerDirection)

        elif navigationDirection == "W":
            if currentSymbol == "L":
                navigationDirection = "N"
                innerDirection = rotateDirection("right", innerDirection)
            elif currentSymbol == "F":
                navigationDirection = "S"
                innerDirection = rotateDirection("left", innerDirection)


    # now let's get the position pointed to by the innerDirection
    innerPosition = findInnerPosition(pos, innerDirection)

    if innerPosition not in finalPath and innerPosition not in innerPositions:
        innerPositions.append(innerPosition)
        map[innerPosition[0]] = replaceCharAtStringPosition(map[innerPosition[0]], innerPosition[1], "i")
        floodFill(map, finalPath, innerPositions, innerPosition)

# print(innerPositions)

for ip in innerPositions:
    map[ip[0]] = replaceCharAtStringPosition(map[ip[0]], ip[1], "X")

for pos in finalPath:
    map[pos[0]] = replaceCharAtStringPosition(map[pos[0]], pos[1], " ")

printMap(map)
print("Final result", len(innerPositions))

count = 0
for row in map:
    for symbol in row:
        if symbol == "X":
            count += 1

print(count)


# part 2 - 366 is too low
# in lines 293/294 I tweak the directions, as I don't know beforehand which direction is inside and which is outside
# I tried S/W and got 366. I changed to N/E (which in theory should be equivalent) and got 365.
# 366 is too low. So I tried 367... and it worked!!! There has to be some sort of glitch somewhere, of course. I'm :-O 
