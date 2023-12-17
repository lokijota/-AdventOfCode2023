import numpy as np
from collections import Counter
import re
import copy
from tqdm import tqdm
import time


# functions

# main code

# read all the lines
with open('Challenges/ch14/sample.txt') as f:
    lines = f.read().splitlines()

# parse data file content

# as we'll be doing manipulations, use a np array instead of lists of strings

board = []
for line in lines:
    board.append(np.array(list(line)))

print(board)

# global variables

# functions

def tilt(board):

    # start with row 0
    # go up the columns until we find a 0
    # move if to the first empty position
    # continue to go up the column
    # avoid going to row 0 again -- keep a pointer of where to move something to
    
    return board

def calculateWeight(board):
    return 0

# process data

board = tilt(board)
print(calculateWeight(board))