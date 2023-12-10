import numpy as np
from collections import Counter
import re
import sys

# functions

def findFactor(valueList):
    # calculate deltas between each value
    deltas = []
    for j in range(1, len(valueList)):
        deltas.append(valueList[j] - valueList[j-1])

    # print("Deltas: ", deltas)
    # all the values are equal 
    if min(deltas) == 0 and max(deltas) == 0:
        return []
    else:
        return [deltas[-1]] + findFactor(deltas)

# main code

# read all the lines
with open('input.txt') as f:
    lines = f.read().splitlines()

# global variables

# parse data into data structures
data = []

for line in lines:
    parts = line.split()
    data.append([int(el) for el in parts])

# print(data)

# process
extrapolatedValues = []
for row in data:
    sequence = []

    # print("---")
    factors = findFactor(row)
    
    extrapolatedValues.append(sum(factors) + row[-1])
    # print("Starting sequence", row)
    # print("Factors:", factors, "/ Sum=", sum(factors))
    # print("Added value=", sum(factors) + row[-1])


print("Part 1:", sum(extrapolatedValues))

# 1712613001 is too high
# part 1 - 1708206096