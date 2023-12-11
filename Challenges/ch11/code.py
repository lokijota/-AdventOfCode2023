import numpy as np
from collections import Counter
import re
import copy

# functions


# main code

# read all the lines
with open('input.txt') as f:
    lines = f.read().splitlines()

# find galaxy positions

galaxies = []
emptyRows = []
emptyColumns = []

# emptyRow = '.' * len(lines[0])

for idxRow, row in enumerate(lines):
    for idxCol, symbol in enumerate(row):
        if lines[idxRow][idxCol] == "#":
            galaxies.append([idxRow, idxCol])

rowWithGalaxies = [g[0] for g in galaxies]
colsWithGalaxies = [g[1] for g in galaxies]

# assumes it's a square shape
for j in range(0, len(lines)):

    if j not in rowWithGalaxies:
        emptyRows.append(j)
    
    if j not in colsWithGalaxies:
        emptyColumns.append(j)

print(galaxies)
print(emptyRows)
print(emptyColumns)

# 1. expand the universe

# the lists empty* are ordered in ascending order

# 1.1 expand horizontally

xDisplacement = 0
for er in emptyRows:
    for g in galaxies:
        if g[0] > er + xDisplacement:
            g[0] += 1000000-1 # use just 1 for part 1
    
    xDisplacement += 1000000-1 # use just 1 for part 1

# 1.2 expand vertically

yDisplacement = 0
for er in emptyColumns:
    for g in galaxies:
        if g[1] > er + yDisplacement:
            g[1] += 1000000-1 # use just 1 for part 1
    
    yDisplacement += 1000000-1 # use just 1 for part 1

print(galaxies)

# can't use the empty* lists anymore as they are now out of sync and would need fixing

# 2. Calculate all the manhatan distances

distance = 0

for idxG1, g1 in enumerate(galaxies):
    for g2 in galaxies[:idxG1]:
        # print("Comparing ", g1, "with", g2)
        md = abs(g1[0]-g2[0]) + abs(g1[1]-g2[1])
        distance += md

print(distance)

# part 1 - 9686930
# part 2 - 630729056210 is too high / 630728425490 is the right answer