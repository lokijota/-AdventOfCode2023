import numpy as np
from collections import Counter
import re
import sys

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

for row in mapLines:

    regexResult = re.search("(\w+) = \((\w+), (\w+)\)", row)

    map[regexResult.group(1)] = [ regexResult.group(2), regexResult.group(3)]

# now run the code
instructionPointer = 0

position = "AAA"
count = 0

while position != "ZZZ":

    position = map[position][nextInstruction()]
    count += 1
    # print("Current position is ", position)

print("Part 1 # steps", count)

# part 1 - 20777
