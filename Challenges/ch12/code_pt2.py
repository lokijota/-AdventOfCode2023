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

def consume(sequence, ip, howMany, leaveFree):
    # Can only consume if followed by . or end of the sequence

    lenSeq = len(sequence)-ip
    # skip dots which have no use here
    while lenSeq > 0 and sequence[ip] == ".":
        # sequence = sequence[1:]
        ip += 1
        lenSeq -= 1

    if lenSeq < howMany:
        return None # i.e. it's not possible to consume the howMany strings

    remainingToConsume = []

    while lenSeq >= howMany and lenSeq >= howMany+leaveFree: 

        nextChar = "" if lenSeq == howMany else sequence[ip + howMany]
        if nextChar != "#": # because if it's a # it means there's a # right after the howMany characters, so this is not a valid config / let's shift right

            if "." not in sequence[ip:ip+howMany]:
                # remainingToConsume.append(sequence[howMany+1:])
                remainingToConsume.append(ip + howMany + 1)

        if sequence[ip] == "#": # we know we don't need to look more, the start has to start here
            return remainingToConsume if len(remainingToConsume) > 0 else None

        # sequence = sequence[1:] # evitar isto e usar um instruction pointer?dir -- e na verdade posso avançar para a posição a seguir ao último ".", se chegar aqui, e poupar uns ciclos
        ip += 1
        lenSeq -= 1

    return remainingToConsume

# this was taking forever and would not get past row 67, so I tried replacing a dictionary with the # of leftovers starting at each given index position... and it went down to 0.17 seconds.
# Proud, even if made a lot of silly thinking mistakes on the way there.
def countArrangementsOLD(sequence, hashGroups):
    leftovers = [0] # instruction pointer: start at position of sequence -- make it a set to avoid repetitions
    leftoverspacesum = sum(hashGroups)
    leftoversspacepadding = len(hashGroups)-1

    for hg in hashGroups:
        auxLeftovers = []

        leftoverspacesum -= hg
        leftoversspacepadding -= 1

        for p in leftovers:
            # if sequence == "???????.???????????.???????????.???????????.???????????.???":
            #     print("p:", p, "hg:", hg, "len:", len(leftovers))
        
            poss = consume(sequence, p, hg, leftoverspacesum+leftoversspacepadding) # TODO: e se n sobrarem coisas para os elementos que vêm para a frente? n vale a pena olhar para além daí! ie, somar os hash da frente mais os separadores e n deixar a captura ir olhar para esses
            if poss is not None:
                auxLeftovers += poss

            # há IPs repetidos em aux left overs. mas n podemos simplesmente remover porque a frequência de repetição é importante. 
            # sposso usar uma hash com contadores para saber das repetições e dps processar qd devolve, para ter uma seq de contadores?

        leftovers = auxLeftovers

    # if at the end we have leftovers that have #'s it means they were not fully consummed and are thus invalid, so we have to remove them
    leftovers = [ lo for lo in leftovers if "#" not in sequence[lo:] ]

    return len(leftovers)


def countArrangements(sequence, hashGroups):
    leftovers = {} #[0] # instruction pointer: start at position of sequence -- make it a set to avoid repetitions
    leftovers[0] = 1 # semantics: there's 1 possibility to match the pattern of hashGroups, starting at position 0
    # for j in range(1,len(sequence)):
    #     leftovers[j] = 0

    leftoverspacesum = sum(hashGroups)
    leftoversspacepadding = len(hashGroups)-1

    for hg in hashGroups:
        auxLeftovers = {}
        for j in range(1,len(sequence)+10):
            auxLeftovers[j] = 0

        leftoverspacesum -= hg
        leftoversspacepadding -= 1

        for leftoverstartpos in leftovers.keys():
            # print("---> LOSP", leftoverstartpos, ", count:", leftovers[leftoverstartpos])
            if leftovers[leftoverstartpos] == 0:
                continue

            # if sequence == "???????.???????????.???????????.???????????.???????????.???":
            #     print("p:", p, "hg:", hg, "len:", len(leftovers))
        
            poss = consume(sequence, leftoverstartpos, hg, leftoverspacesum+leftoversspacepadding) # TODO: e se n sobrarem coisas para os elementos que vêm para a frente? n vale a pena olhar para além daí! ie, somar os hash da frente mais os separadores e n deixar a captura ir olhar para esses
            if poss is not None:
                # print(poss)
                # auxLeftovers += poss
                for p in poss:
                    auxLeftovers[p] += leftovers[leftoverstartpos]

            # há IPs repetidos em aux left overs. mas n podemos simplesmente remover porque a frequência de repetição é importante. 
            # sposso usar uma hash com contadores para saber das repetições e dps processar qd devolve, para ter uma seq de contadores?

        leftovers = auxLeftovers

    # if at the end we have leftovers that have #'s it means they were not fully consummed and are thus invalid, so we have to remove them
    for lotestvalid in leftovers.keys():
        if "#" in sequence[lotestvalid:]:
            leftovers[lotestvalid] = 0
            
    # leftovers = [ lo for lo in leftovers if "#" not in sequence[lo:] ]

    soma = 0
    for lo in leftovers.keys():
        soma += leftovers[lo]

    return soma
    # return len(leftovers)

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
for idx, cr in enumerate(conditionRecords):
    arrc = countArrangements(cr[0]+"?"+cr[0]+"?"+cr[0]+"?"+cr[0]+"?"+cr[0], cr[1]+cr[1]+cr[1]+cr[1]+cr[1])
    print("Row", idx, cr[0]+"?"+cr[0]+"?"+cr[0]+"?"+cr[0]+"?"+cr[0], cr[1]+cr[1]+cr[1]+cr[1]+cr[1], " -> ", arrc)
    arrangementCount += arrc

aaa = countArrangements("?###??????????###??????????###??????????###??????????###????????", [3,2,1,3,2,1,3,2,1,3,2,1,3,2,1])
print("banana", aaa)


print("--- %s seconds ---" % (time.time() - start_time))

print("Number of arrangements:", arrangementCount)

# part 1:
# 7405 is too high
# 4899 is too low
# 5105 is too low
# 7366 is not the right answer
# right - 7169

# for part 2, after hours of work, replacing the lisrts with a dictionary with counts...:

# --- 0.17371892929077148 seconds ---
# Number of arrangements: 1738259948652
