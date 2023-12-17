import numpy as np
from collections import Counter
import re
import copy
from tqdm import tqdm
import time


# functions

# main code

# read all the lines
with open('Challenges/ch13/input.txt') as f:
    lines = f.read().splitlines()

# parse data file content

lines = [line.replace("#", "1").replace(".", "0") for line in lines ]

squares = []
rowValues = []
for line in lines:

    if len(line) > 0:
         rowValues.append(list(line))
    else:
         squares.append(np.array(rowValues))
         rowValues = []

# print(squares)

# global variables

# functions
def findFold(square):
     
    for foldPosition in range(1, len(square[0])):

        # find the intervals for each different separator position 
        leftstart = 0
        leftend = foldPosition-1
        
        rightstart = foldPosition
        rightend = foldPosition + leftend
        if rightend > len(square[0])-1:
            rightend = len(square[0])-1

        leftstart = leftend - (rightend - rightstart)

        # print(leftstart, "to", leftend, "and", rightstart, "to", rightend)

        areNotEqual = False
        for row in square:
            leftPart = row[leftstart:leftend+1]
            rightPart = row[rightstart:rightend+1]
            rightPart = rightPart[::-1]
            # print(leftPart, "=", rightPart)

            if not(all(leftPart == rightPart)):
            # if leftPart != rightPart:
                areNotEqual = True
                break

        if areNotEqual == False:
            return leftend+1
        
    return -1


# process data

sumCols = 0
sumRows = 0

for square in squares:
    foldPos = findFold(square)

    if foldPos >= 0:
        sumCols += foldPos
        print("  Col fold:", foldPos)
        continue
    
    # print("Square", square)
    # print("Transpose", np.transpose(square))

    foldPos = findFold(np.transpose(square))

    if foldPos == -1:
        foldPos = 0

    sumRows += foldPos
    print("  Row fold:", foldPos)

print("Part 1 - ", sumCols + sumRows*100)

# 23074 is too low
# 24674 is too low
# 33972 is too low
# -> 34772


# Part 2
sumCols = 0
sumRows = 0

def findFolds(square):
    foldsFound = set()

    for foldPosition in range(1, len(square[0])):

        # find the intervals for each different separator position 
        leftstart = 0
        leftend = foldPosition-1
        
        rightstart = foldPosition
        rightend = foldPosition + leftend
        if rightend > len(square[0])-1:
            rightend = len(square[0])-1

        leftstart = leftend - (rightend - rightstart)

        areNotEqual = False
        for row in square:
            leftPart = row[leftstart:leftend+1]
            rightPart = row[rightstart:rightend+1]
            rightPart = rightPart[::-1]

            if not(all(leftPart == rightPart)):
                areNotEqual = True
                break

        if areNotEqual == False:
            foldsFound.add(leftend+1)
        
    return foldsFound

def testCombinations(square):
    solutions = set()

    for r in range(0, len(square)):
        for c in range(0, len(square[0])):

            square[r][c] = "1" if square[r][c] == "0" else "0"
            foldsPos = findFolds(square)

            # restore previous value
            square[r][c] = "1" if square[r][c] == "0" else "0"

            solutions = solutions.union(foldsPos)

    return solutions

for square in squares:

    # check the columns
    foldPos = findFold(square)
    foldPosAfterFlips = testCombinations(square)
    if foldPos in foldPosAfterFlips:
        foldPosAfterFlips.remove(foldPos)

    if len(foldPosAfterFlips) > 0:
        # print(foldPosAfterFlips)

        for colfold in foldPosAfterFlips:
            sumCols += colfold
            print("  Col fold:",colfold)
        continue
    
    # check the rows
    transposedSquare = np.transpose(square)

    foldPos = findFold(transposedSquare)
    foldPosAfterFlips = testCombinations(transposedSquare)
    if foldPos in foldPosAfterFlips:
        foldPosAfterFlips.remove(foldPos)

    if len(foldPosAfterFlips) > 0:
        # print(foldPosAfterFlips)

        for rowfold in foldPosAfterFlips:
            sumRows += rowfold
            print("  Row fold:", rowfold)
        continue

print("Part 2 - ", sumCols + sumRows*100)

# part 2 - 35554