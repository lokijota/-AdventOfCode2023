import numpy as np
from collections import Counter
import re
import copy
from tqdm import tqdm
import time

# functions

# main code

# read all the lines
with open('Challenges/ch14/input.txt') as f:
    lines = f.read().splitlines()

# parse data file content

# as we'll be doing manipulations, use a np array instead of lists of strings

board = []
for line in lines:
    # print(line)
    # board.append(np.array(list(line)))

    line = list(line.replace(".", "0").replace("O", "8").replace("#","1"))
    line = [int(el) for el in line]
    # board.append(np.array(line))
    board.append(line)

# change from list of arrays into array of arrays/bidimensional array
board = np.array(board)

# print(board)

# global variables

# functions

def moveup(board, col, iprow):
    while iprow < len(board) and board[iprow][col] in [ 1, 8 ]:
        iprow += 1

    return iprow

def tilt(board):

    for col in range(0, len(board[0])):

        row = 0
        iprow = 0

        # find starting position for ip
        while board[iprow][col] != 0:
            iprow += 1
            row = iprow+1

        # now start the movements
        # print("--")
        while row < len(board):
            if board[row][col] == 1:
                iprow = moveup(board, col, row) # note: row

            elif board[row][col] == 8:
                if row > iprow:
                    board[iprow][col] = 8
                    board[row][col] = 0
                    iprow += 1

                iprow = moveup(board, col, iprow)

                # for r in board:
                #     print(r)

            row += 1

    return board


def calculateWeight(board):

    # print("calculateWeight:")
    # for r in board:
    #     print(r)
    
    weight = 0

    for c in range(0, len(board[0])):
        for r in range(0, len(board)):

            if board[r][c] == 8:
                weight += len(board)-r

                # for _ in range(r, len(board)):
                #     weight += 1

        # print("after col", c, "weight=", weight)

    return weight

# process data

start_time = time.time()

# commented out to run for part 2
# board = tilt(board)
# print("Result part 1: ", calculateWeight(board))

# print("--- %s seconds ---" % (time.time() - start_time))

# part 1 - 109833, 0.012 - 0.007 secs : usando strings para representar o mapa
# part 1 - 109833, 0.009 - 0.007 secs : usando integers para representar o mapa
# part 1 - 109833, 0.010 - 0.009 secs : using np 2-dim array instead of list of np arrays became slightly slower... odd. 

# part 2

start_time = time.time()

firstZeroPos = 0 # first position where first weightN - weightN-1 = 0 -- start of a repeating cycle
secondZeroPos = 0 # second position where first weightN - weightN-1 = 0  -- end of a repeating cycle
repeatingSequence = []
prevWeight = 0

for cycleCount in range(0,1000000000):
    for directions in ["W", "S", "E", "N"]:
        board = tilt(board)
        board = np.rot90(board,3)
    
    if cycleCount > 100: # why this? well, in the sample there's two 0's one after the other, so I'm moving it forward.
        # I could also consider any number as the start of the repeating cycle, after moving forward a certain number of repetitions, but it works like this, and 0 delta
        # *IS* the start of the loop
        weight = calculateWeight(board)

        if weight-prevWeight == 0 and firstZeroPos == 0:
            firstZeroPos = cycleCount
        elif weight-prevWeight == 0 and firstZeroPos > 0:
            secondZeroPos = cycleCount
            break

        if firstZeroPos > 0:
            repeatingSequence.append(weight)

        prevWeight = weight

print("Repeating sequence: ", repeatingSequence)
posOfResult = (1000000000-firstZeroPos) % (secondZeroPos-firstZeroPos) - 1
print("Result part 2: : ", repeatingSequence[posOfResult])


print("--- %s seconds ---" % (time.time() - start_time))

# print("final:")
# for r in board:
#     print(r)

# 99849 is too low
# 99875 is the right for part 2

# see the excel file for the logic