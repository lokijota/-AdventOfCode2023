import numpy as np
from collections import Counter
import re
import sys

# functions

def findFactor(valueList):
    # calculate deltas between each value. this doesn't depend on what we do with them later on
    deltas = []
    for j in range(1, len(valueList)):
        deltas.append(valueList[j] - valueList[j-1])

    print("Deltas: ", deltas)
    # all the values are equal 
    if min(deltas) == 0 and max(deltas) == 0:
        return []
    else:
        return [deltas[0]] + findFactor(deltas)

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

    print("---")
    factors = findFactor(row)

    # calculate factor sum
    sumFactors = 0
    sign = 1
    for f in factors:
        sumFactors = sumFactors + f*sign
        sign *= -1
    print("sf = ", sumFactors)
    
    extrapolatedValues.append(row[0] - sumFactors)
    print("Starting sequence", row)
    print("Factors:", factors, "/ Sum=", sumFactors)
    print("row[0]", row[0])
    print("Added value=", row[0] - sumFactors)

print("Extrapolated Values", extrapolatedValues)
print("Part 2:", sum(extrapolatedValues))

# 914341033 is too high
# part 2 answer is 1050