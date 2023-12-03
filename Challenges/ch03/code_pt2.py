import numpy as np
import re

# functions

# generate positions surrounding a number
def generatePositions(rowNb, colStart, colEnd):
    positions = []

    # top and bottom including corners
    for col in range(colStart-1, colEnd+1):
        positions.append((rowNb-1, col))
        positions.append((rowNb+1, col))
    
    # start and end
    positions.append((rowNb, colStart-1))
    positions.append((rowNb, colEnd))

    return positions

# check if it's surrounded by a symbol (star)
def surroundingSymbol(map, positions):

    for position in positions:

        # print("Pos: ", position[0], position[1])

        mapCharacter = map[position[0]][position[1]]

        # part 2 change
        if mapCharacter == '*':
            print(position, "-- is surrounded by star")
            return position
    
    print("-- is not surrounded by star")
    return None

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

# print(lines)
# print(map)

starPositionsAndOperands = {}

for rowNb, mapRow in enumerate(map):
    matches = re.finditer("(\d+)", mapRow)

    print("RowNb:", rowNb)

    for matchNum, match in enumerate(matches, start=1):
        # find number
        print(match.start(), match.end(), match.group())

        # generate all the surounding positions
        surroundingPositions = generatePositions(rowNb, match.start(), match.end())
        starPosition = surroundingSymbol(map, surroundingPositions)

        if starPosition is not None:
            key = str(starPosition[0]) + "_" + str(starPosition[1])
            if key in starPositionsAndOperands:
                starPositionsAndOperands[key].append(int(match.group()))
            else:
                starPositionsAndOperands[key] = [ int(match.group()) ]


# now go over the hashtable and if there's 2 elements in a hash element, multiply them and add
sum = 0

for hashElementKey in starPositionsAndOperands.keys():
    if len(starPositionsAndOperands[hashElementKey]) == 2:
        sum += starPositionsAndOperands[hashElementKey][0] * starPositionsAndOperands[hashElementKey][1]

print(sum)


# 4361 is too low - it's the sample
# 84266818 for part 2