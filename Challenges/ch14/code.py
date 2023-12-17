import numpy as np
from collections import Counter
import re
import copy
from tqdm import tqdm
import time


# functions

# O....#....
# O.OO#....#
# .....##...
# OO.#O....O
# .O.....O#.
# O.#..O.#.#
# ..O..#O..O
# .......O..
# #....###..
# #OO..#....

# main code

# read all the lines
with open('Challenges/ch14/sample.txt') as f:
    lines = f.read().splitlines()

# parse data file content

# as we'll be doing manipulations, use a np array instead of lists of strings

board = []
for line in lines:
    board.append(np.array(list(line)))

# print(board)

# global variables

# functions

def moveup(board, col, iprow):
    while iprow < len(board) and board[iprow][col] in [ "#", "O" ]:
        iprow += 1

    return iprow

def tilt(board):

    for col in range(0, len(board[0])):

        row = 0
        iprow = 0

        # find starting position for ip
        while board[iprow][col] != ".":
            iprow += 1
            row = iprow+1

        # now start the movements
        print("--")
        while row < len(board):
            if board[row][col] == "#":
                iprow = moveup(board, col, row) # note: row

            elif board[row][col] == "O":
                if row > iprow:
                    board[iprow][col] = "O"
                    board[row][col] = "."
                    iprow += 1

                iprow = moveup(board, col, iprow)

                for r in board:
                    print(r)

            row += 1

    return board

def calculateWeight(board):
    return 0

# process data

for r in board:
    print(r)
board = tilt(board)
print("tilted:")
for r in board:
    print(r)

print("Result part 1: ", calculateWeight(board))