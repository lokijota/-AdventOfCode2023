import numpy as np
from collections import Counter
import re
import copy
from tqdm import tqdm
import time
from collections import deque
import random

# functions

# main code

# read all the lines
with open('Challenges/ch17/input.txt') as f:
    lines = f.read().splitlines()

# parse data file content

nrows = len(lines)
ncols = len(lines[0])
map = lines


for r in range(0,nrows):
    for c in range(0,ncols):
        if int(map[r][c]) == 9: #< 6 and int(map[r][c]) > 4 :
            print(map[r][c], end="")
        else:
            print(" ", end="")

    print()