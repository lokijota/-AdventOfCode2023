import numpy as np
import re

# functions


# main code

# read all the lines
with open('input.txt') as f:
    lines = f.read().splitlines()

# global variables
winningDictionary = {}
handDictionary = {}
points = 0

# parse data and feed dictionary
for line in lines:
    parts = line.split(':')

    cardNb = int(parts[0].replace("Card ", "").strip())
    print("Card ", cardNb)

    numberParts = parts[1].strip().split("|")

    winningNbs = numberParts[0].strip().split(" ")
    handNbs = numberParts[1].strip().split(" ")

    # now find how many of the numbers on the first are on the second
    winningInHand = [x for x in handNbs if x in winningNbs and len(x) > 0]
    print("  Winning in Hand: ", winningInHand)

    if len(winningInHand) > 0:
        points += 2**(len(winningInHand)-1)

    print("  New score: ", points)

# 103579 is too high
# 18519 part 1 good
