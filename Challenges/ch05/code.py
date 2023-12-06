import numpy as np
import re
import sys

# functions
def mapThing(mapper, operand):
    # print("mapping ", mapper[0], " to ", mapper[1])

    for mapRule in mapper[2]:
        if operand >= mapRule[1] and operand < mapRule[1] + mapRule[2]: # or <= ?
            return operand - mapRule[1] + mapRule[0]

    return operand

# main code

# read all the lines
with open('input.txt') as f:
    lines = f.read().splitlines()

# global variables
seeds = []
mappers = []
currentMapper = None

# parse data into data structures
for line in lines:

    if len(line) == 0:
        if currentMapper is not None:
            mappers.append(currentMapper)
            currentMapper = None
        continue

    if line.startswith("seeds:"):
        line = line.replace("seeds: ", "")
        parts = line.split(" ")
        seeds = [int(x) for x in parts]
        continue

    if line == "seed-to-soil map:":
        currentMapper = [ "seed", "soil", []]
        continue
    elif line == "soil-to-fertilizer map:":
        currentMapper = [ "soil", "fertilizer", []]
        continue
    elif line == "fertilizer-to-water map:":
        currentMapper = [ "fertilizer", "water", []]
        continue
    elif line == "water-to-light map:":
        currentMapper = [ "water", "light", []]
        continue
    elif line == "light-to-temperature map:":
        currentMapper = [ "light", "temperature", []]
        continue
    elif line == "temperature-to-humidity map:":
        currentMapper = [ "temperature", "humidity", []]
        continue
    elif line == "humidity-to-location map:":
        currentMapper = [ "humidity", "location", []]
        continue

    # else
    parts = line.split(" ")
    parts = [int(x) for x in parts]
    currentMapper[2].append(parts)

if currentMapper is not None:
    mappers.append(currentMapper)

print(mappers)

# now run the maps for part 1
# minLocation = sys.maxsize

# for seed in seeds:

#     operand = seed
#     for mapper in mappers:

#         after = mapThing(mapper, operand)
#         print("  mapped ", operand, " to ", after)
#         operand = after

#     if operand < minLocation:
#         minLocation = operand
#     print("-----")

# print("Part 1 - MININUM: ", minLocation)

# 261668924 part 1

# now run the maps for part 2
minLocation = sys.maxsize

# group the seeds into pairs
# https://stackoverflow.com/questions/1624883/alternative-way-to-split-a-list-into-groups-of-n
seeds = [seeds[i:i+2] for i in range(0, len(seeds), 2)]
print(seeds)

for seed in seeds:
    # print("Seed: ", seed)
    for i in range(seed[0], seed[0] + seed[1]):

        # print("  seed in loop ", i)
        operand = i
        for mapper in mappers:

            after = mapThing(mapper, operand)
            # print("  mapped ", operand, " to ", after)
            operand = after

        if operand < minLocation:
            minLocation = operand
            print("  New min is ", minLocation)
        # else:
        #     print("  NOT min is ", operand)

    
print("Part 2 - MININUM: ", minLocation)

# 24.261.546 is too high
# 24.261.545 is the right answer