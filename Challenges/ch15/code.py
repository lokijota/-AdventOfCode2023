import numpy as np
from collections import Counter
import re
import copy
from tqdm import tqdm
import time

# functions

# main code

# read all the lines
with open('Challenges/ch15/sample.txt') as f:
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
    result += calculateHash(step)

print("Result part 1: ", result) # 517551

print("--- %s seconds ---" % (time.time() - start_time))

# part 2
