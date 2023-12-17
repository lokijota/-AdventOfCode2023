import numpy as np
from collections import Counter
import re
import copy
from tqdm import tqdm
import time

# functions

# main code

# read all the lines
with open('Challenges/ch15/input.txt') as f:
    lines = f.read().splitlines()

# parse data file content

steps = lines[0].split(",")

# global variables

# functions

# Determine the ASCII code for the current character of the string.
# Increase the current value by the ASCII code you just determined.
# Set the current value to itself multiplied by 17.
# Set the current value to the remainder of dividing itself by 256.
def calculateHash(string):

    hash = 0

    for letra in string:
        hash += ord(letra)
        hash *= 17
        hash %= 256

    return hash

# process data

start_time = time.time()

# result = calculateHash("HASH")
result = 0

for step in steps:

    # print(step, calculateHash(step))
    result += calculateHash(step)


print("Result part 1: ", result) # 517551

print("--- %s seconds ---" % (time.time() - start_time))

# part 2

lightbox = []
for i in range(0, 256):
    lightbox.append([])

for step in steps:

    # parse each instruction
    if step.endswith("-"):
        boxcode = step[:-1]
        operator = "-"
        lens = 0
    else:
        parts = step.split("=")
        boxcode = parts[0]
        operator = "="
        lens = int(parts[1])

    # print(boxcode, operator, lens)

    # now parse the instructions

    box = calculateHash(boxcode)

    if operator == "-":
        # remove
        lightbox[box] = [tup for tup in lightbox[box] if tup[0] != boxcode]
        # foo = [x for x in foo if x!= ("Alba", "Texas")]

    else:
        # add or replace
        isItThere = [tup for tup in lightbox[box] if tup[0] == boxcode]

        if len(isItThere) == 0:
            lightbox[box].append( (boxcode, lens) )
        else:
            lightbox[box] = [(tup[0], lens) if tup[0] == boxcode else tup for tup in lightbox[box]]


# calculate result

# To confirm that all of the lenses are installed correctly, add up the focusing power of all of the lenses. 
# The focusing power of a single lens is the result of multiplying together:

# One plus the box number of the lens in question.
# The slot number of the lens within the box: 1 for the first lens, 2 for the second lens, and so on.
# The focal length of the lens.

result = 0
for boxnb in range(0, 256):

    for slotNb in range(0, len(lightbox[boxnb])):
        result += (boxnb+1) * (slotNb+1) * lightbox[boxnb][slotNb][1]

print("Result part 2: ", result) # 286097
