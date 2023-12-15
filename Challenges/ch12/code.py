import numpy as np
from collections import Counter
import re
import copy
from tqdm import tqdm
import time


# e se tentar consumir as coisas como se fosse BNF? i.e., partir dos números em vez de partir da sequência
# ter uma funç\ao de "get(n) que devolve alternativas de remaining strings consumidas para ser processsadas pelo numero seguinte na lista"

# functions

combinationsCache = {}

def consume(sequence, howMany, leaveFree):
    # Can only consume if followed by . or end of the sequence

    lenSeq = len(sequence)
    # skip dots which have no use here
    while lenSeq > 0 and sequence[0] == ".":
        sequence = sequence[1:]
        lenSeq -= 1

    if lenSeq < howMany:
        return None # i.e. it's not possible to consume the howMany strings

    remainingToConsume = []

    while lenSeq >= howMany and lenSeq >= howMany+leaveFree: 

        nextChar = "" if lenSeq == howMany else sequence[howMany]
        if nextChar != "#": # because if it's a # it means there's a # right after the howMany characters, so this is not a valid config / let's shift right

            if "." not in sequence[:howMany]:
                remainingToConsume.append(sequence[howMany+1:])

        if sequence[0] == "#": # we know we don't need to look more, the start has to start here
            return remainingToConsume if len(remainingToConsume) > 0 else None

        sequence = sequence[1:] # evitar isto e usar um instruction pointer?dir -- e na verdade posso avançar para a posição a seguir ao último ".", se chegar aqui, e poupar uns ciclos
        lenSeq -= 1

    return remainingToConsume

def countArrangements(sequence, hashGroups):
    leftovers = [sequence]
    leftoverspacesum = sum(hashGroups)
    leftoversspacepadding = len(hashGroups)-1

    for hg in hashGroups:
        auxLeftovers = []

        leftoverspacesum -= hg
        leftoversspacepadding -= 1

        for p in leftovers:
            poss = consume(p, hg, leftoverspacesum+leftoversspacepadding) # TODO: e se n sobrarem coisas para os elementos que vêm para a frente? n vale a pena olhar para além daí! ie, somar os hash da frente mais os separadores e n deixar a captura ir olhar para esses
            if poss is not None:
                auxLeftovers += poss

        leftovers = auxLeftovers

    # if at the end we have leftovers that have #'s it means they were not fully consummed and are thus invalid, so we have to remove them
    leftovers = [lo for lo in leftovers if "#" not in lo ]

    return len(leftovers)

# main code

# read all the lines
with open('Challenges/ch12/input.txt') as f:
    lines = f.read().splitlines()

# global variables

# https://stackoverflow.com/questions/1867861/how-to-keep-keys-values-in-same-order-as-declared
conditionRecords = []

# parse data into data structures
for line in lines:
    parts = line.split()
    damagedSprings = parts[1].split(",")
    conditionRecords.append([parts[0], [int(ds) for ds in damagedSprings]])

# process data
arrangementCount = 0

start_time = time.time()

# for cr in tqdm(conditionRecords):
for cr in conditionRecords:
    arrc = countArrangements(cr[0]+"?"+cr[0]+"?"+cr[0]+"?"+cr[0]+"?"+cr[0], cr[1]+cr[1]+cr[1]+cr[1]+cr[1])
    print(cr[0]+"?"+cr[0]+"?"+cr[0]+"?"+cr[0]+"?"+cr[0], cr[1]+cr[1]+cr[1]+cr[1]+cr[1], " -> ", arrc)
    arrangementCount += arrc

print("--- %s seconds ---" % (time.time() - start_time))

print("Number of arrangements:", arrangementCount)

# part 1:
# 7405 is too high
# 4899 is too low
# 5105 is too low
# 7366 is not the right answer
# right - 7169