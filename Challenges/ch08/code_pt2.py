import numpy as np
from collections import Counter
import re

# functions

instructions = None

def nextInstruction():
    global instructionPointer

    instruction = instructions[instructionPointer]
    instructionPointer += 1
    if instructionPointer == len(instructions):
        instructionPointer = 0

    if instruction == "L":
        return 0
    else:
        return 1

# main code

# read all the lines
with open('input.txt') as f:
    lines = f.read().splitlines()

# global variables

# parse data into data structures
instructions = lines[0]
mapLines = lines[2:]
map = {}

currentPositions = []

for row in mapLines:

    regexResult = re.search("(\w+) = \((\w+), (\w+)\)", row)

    map[regexResult.group(1)] = [ regexResult.group(2), regexResult.group(3)]

    if regexResult.group(1).endswith("A"):
        currentPositions.append(regexResult.group(1))


# now run the code
instructionPointer = 0
count = 0

print("Starting positions: ", currentPositions)

periodicity = {}
countPeriodicityFound = 0
while countPeriodicityFound < len(currentPositions):
    ip = nextInstruction()

    currentPositions = [map[pos][ip] for pos in currentPositions]

    count += 1

    for idx in range(0, len(currentPositions)):
        if currentPositions[idx][-1] == "Z" and "col" + str(idx) not in periodicity:
            periodicity["col" + str(idx)] = count
            countPeriodicityFound += 1

print("Periodicidades: ", periodicity)

# Now let's look at the heights of columns only
maxPeriod = max(periodicity.values())
listPeriods = list(periodicity.values())
foundIt = False
count = maxPeriod

print("How many columns?", len(currentPositions))
while foundIt == False:

    # print("Count", count)

    foundIt = True
    for idx in range(0, len(currentPositions)):
        if count % listPeriods[idx] != 0:
            foundIt = False
            break

    if foundIt == True:
        break
    else:
        count += maxPeriod


print("Part 2 # steps", count)

# part 2: 13289612809129


# note: this is a dumb way of doing it, but still takes ~6 minutes. You can also look at the repetitions with the len of the instruction sequence, 
# and knowing that the periodicities ("column heights") always start with zero, us the # of loops of the instruction sequence,
# and then find the factors
