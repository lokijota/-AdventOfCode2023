import numpy as np
from collections import Counter
import re
import copy


# e se tentar consumir as coisas como se fosse BNF? i.e., partir dos números em vez de partir da sequência
# ter uma funç\ao de "get(n) que devolve alternativas de remaining strings consumidas para ser processsadas pelo numero seguinte na lista"

# functions

combinationsCache = {}

def consume(sequence, howMany):
    # Can only consume if followed by . or end of the sequence

    # skip dots which have no use here
    while len(sequence) > 0 and sequence[0] == ".":
        sequence = sequence[1:]

    if len(sequence) < howMany:
        return None # i.e. it's not possible to consume the howMany strings

    # first (simple) case: there is the howMany number of #'s followed by EOS or a . // can also be followed by a ? in which case i's valid

    # generate combinations
    if str(howMany) not in combinationsCache:
        combinations = [ "#", "?"]
        for _ in range(0,howMany-1):
            auxCombinations = []
            for c in combinations:
                auxCombinations.append(c + "#")
                auxCombinations.append(c + "?")

            combinations = auxCombinations

        combinationsCache[str(howMany)] = combinations
    combinations = combinationsCache[str(howMany)]


    remainingToConsume = []
    while len(sequence) >= howMany: # estamos a consumir todos os caracteres da string, o que n faz sentido / isto poderia ser optimizado

        nextChar = "" if len(sequence) == howMany else sequence[howMany]
        if nextChar != "#": # because if it's a # it means there's a # right after the howMany characters, so this is not a valid config / let's shift right
            for c in combinations:
                if sequence.startswith(c): # and nextChar in ["", ".", "?"]: # all but # !
                    remainingToConsume.append(sequence[howMany+1:].strip()) # only the remaining string (to the right) is returned for further processing by other numbers
                    # +1 to remove the next character after a match -- has to be a . or ? (note the nextChar if, above)
                    # print("    Possible match at start with", c, "on sequence", sequence,"remaining sequence is", sequence[howMany+1:])

        if "#" in sequence[0]: # we know we don't need to look more, the start has to start here
            return remainingToConsume if len(remainingToConsume) > 0 else None


        sequence = sequence[1:]

    return remainingToConsume

def countArrangements(sequence, hashGroups):
    leftovers = [sequence]

    # print("countArrangements", sequence)
    for hg in hashGroups:
        # print("------------ Consumming #chars", hg)
        auxLeftovers = []

        for p in leftovers:
            poss = consume(p, hg) # TODO: e se n sobrarem coisas para os elementos que vêm para a frente? n vale a pena olhar para além daí! ie, somar os hash da frente mais os separadores e n deixar a captura ir olhar para esses
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

for cr in conditionRecords:
    arrc = countArrangements(cr[0], cr[1])
    print(cr[0], cr[1], " -> ", arrc)
    arrangementCount += arrc

print("Number of arrangements:", arrangementCount)

# 7405 is too high
# 4899 is too low
# 5105 is too low
# 7366 is not the right answer


# right - 7169