import numpy as np
import re
import sys

# functions


# main code

# read all the lines
with open('input_pt2.txt') as f:
    lines = f.read().splitlines()

# global variables

# parse data into data structures
for line in lines:
    if line.startswith("Time:"):
        line = line.replace("Time: ", "").strip()
        times = line.split()
    
    if line.startswith("Distance:"):
        line = line.replace("Distance: ", "").strip()
        distances = line.split()

races = [[int(times[i]), int(distances[i])] for i in range(0, len(times))]
print(races)

totals = np.zeros(len(races), dtype=int)

for idx, race in enumerate(races):

    for velocity in range(1, race[0]-1):
        movementTime = race[0]-velocity
        distance = movementTime * velocity

        if distance > race[1]:
            totals[idx] += 1

    print(totals[idx])

print("Score: ", np.prod(totals))

# part 1 - 2374848
# part 2 - 39132886 (just took a new file, ran fast -- no code changes)