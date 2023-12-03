import numpy as np
import re

# functions
def generatePositions(rowNb, colStart, colEnd):
    positions = []

    # top and bottom including corners
    for col in range(colStart-1, colEnd+1):
        positions.append((rowNb-1, col))
        positions.append((rowNb+1, col))
    
    # start and end
    positions.append((rowNb, colStart-1))
    positions.append((rowNb, colEnd))

    # print("generatePositions for:", rowNb, colStart, colEnd)
    # print(positions)

    return positions

def surroundingSymbol(map, positions):

    for position in positions:

        # print("Pos: ", position[0], position[1])

        mapCharacter = map[position[0]][position[1]]

        if mapCharacter != '.' and not mapCharacter.isdigit():
            print("-- is surrounded")
            return True
    
    print("-- is not surrounded")
    return False

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

sum = 0

for rowNb, mapRow in enumerate(map):
    matches = re.finditer("(\d+)", mapRow)

    print("RowNb:", rowNb)

    for matchNum, match in enumerate(matches, start=1):
        # find number
        print(match.start(), match.end(), match.group())

        # generate all the surounding positions
        surroundingPositions = generatePositions(rowNb, match.start(), match.end())

        if surroundingSymbol(map, surroundingPositions):
            sum += int(match.group())

# check if there's a separating
# if so, count as number
# move to next

print(sum)


# 4361 is too low - it's the sample
# 557705 for part 1