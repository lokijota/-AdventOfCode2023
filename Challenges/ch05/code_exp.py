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

def reverseMap(boundaries, mapper):
    mapped = []
    processed = []

    for mapRule in mapper[2]:
        for boundary in boundaries:
            if boundary == mapRule[0]:
                mapped.append(mapRule[1])
                processed.append(boundary)

    # all the ones that were not mapped must be added as is to the target
    [mapped.append(x) for x in boundaries if x not in processed]

    # print("mapped: ", mapped)
    return mapped
# main code

# read all the lines
with open('sample.txt') as f:
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


# now run the maps for part 2
minLocation = sys.maxsize

# group the seeds into pairs
# https://stackoverflow.com/questions/1624883/alternative-way-to-split-a-list-into-groups-of-n
seeds = [seeds[i:i+2] for i in range(0, len(seeds), 2)]
print(seeds)



boundaries = []
for mapper in reversed(mappers):
    for mapRule in mapper[2]:
        boundaries.append(mapRule[0])
        boundaries.append(mapRule[0] + mapRule[2])

    boundaries.sort()
    boundaries = list(dict.fromkeys(boundaries))
    print("Boundaries:", boundaries)
    reverseMap(boundaries, mapper)

print("final boundaries: ", boundaries)
        # if operand >= mapRule[1] and operand < mapRule[1] + mapRule[2]: # or <= ?
        #     return operand - mapRule[1] + mapRule[0]




for boundary in boundaries:
    for seed in seeds:

        if boundary >= seed[0] and boundary < seed[0] + seed[1]:
            operand = boundary
            
            for mapper in mappers:
                after = mapThing(mapper, operand)
                print("  mapped ", operand, " to ", after)
                operand = after

            if operand < minLocation:
                minLocation = operand
            print("-----")


print("Part 2 - MININUM: ", minLocation)

# 24.261.546 is too high