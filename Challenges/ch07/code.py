import numpy as np
from collections import Counter
import re
import sys

# functions

def findHandType(hand):
    # 6 - Five of a kind, where all five cards have the same label: AAAAA
    # 5 - Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    # 4 - Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    # 3 - Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    # 2 - Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    # 1 - One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    # 0 - High card, where all cards' labels are distinct: 23456

    c = Counter(hand) # eg - Counter({'3': 2, '2': 1, 'T': 1, 'K': 1})
    frequenciesList = list(c.values())

    if len(frequenciesList) == 1:
        # five of a kind
        return 700000000
    elif len(frequenciesList) == 2:
        # four of a kind or full-house
        if frequenciesList[0] == 4 or frequenciesList[1] == 4:
            return 600000000
        else:
            return 500000000
    elif len(frequenciesList) == 3:
        # three of a kind or two pair
        if frequenciesList[0] == 3 or frequenciesList[1] == 3 or frequenciesList[2] == 3:
            return 400000000
        else:
            return 300000000
    elif len(frequenciesList) == 4:
        # one pair
        return 200000000
    elif len(frequenciesList) == 5:
        # all different
        return 100000000

    return -1


# adapted from: https://www.geeksforgeeks.org/python-program-for-quicksort/

# Function to find the partition position
def partition(array, low, high):
 
    # choose the rightmost element as pivot
    pivot = array[high]
 
    # pointer for greater element
    i = low - 1
 
    # traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if array[j][4] <= pivot[4]:
 
            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1
 
            # Swapping element at i with element at j
            (array[i], array[j]) = (array[j], array[i])
 
    # Swap the pivot element with the greater element specified by i
    (array[i + 1], array[high]) = (array[high], array[i + 1])
 
    # Return the position from where partition is done
    return i + 1
 
# function to perform quicksort
 
def quickSort(array, low, high):
    if low < high:
 
        # Find pivot element such that element smaller than pivot are on the left, element greater than pivot are on the right
        pi = partition(array, low, high)
 
        # Recursive call on the left of pivot
        quickSort(array, low, pi - 1)
 
        # Recursive call on the right of pivot
        quickSort(array, pi + 1, high)



# main code

# read all the lines
with open('input.txt') as f:
    lines = f.read().splitlines()

# global variables

# parse data into data structures

data = []
for line in lines:
    parts = line.split()

    # convert the hand in hex
    hexRepr = parts[0]
    hexRepr = hexRepr.replace('2', '0')
    hexRepr = hexRepr.replace('3', '1')
    hexRepr = hexRepr.replace('4', '2')
    hexRepr = hexRepr.replace('5', '3')
    hexRepr = hexRepr.replace('6', '4')
    hexRepr = hexRepr.replace('7', '5')
    hexRepr = hexRepr.replace('8', '6')
    hexRepr = hexRepr.replace('9', '7')
    hexRepr = hexRepr.replace('T', '8')
    hexRepr = hexRepr.replace('J', '9')
    hexRepr = hexRepr.replace('Q', '_') # note temp replace
    hexRepr = hexRepr.replace('K', 'B')
    hexRepr = hexRepr.replace('A', 'C')
    hexRepr = hexRepr.replace('_', 'A') # note
    hexRepr = "0x" + hexRepr
    intCardValues = int(hexRepr, 0)

    # identity that type of hand it is
    handType = findHandType(parts[0])

    # https://stackoverflow.com/questions/209513/convert-hex-string-to-integer-in-python
    data.append([parts[0], int(parts[1]), int(hexRepr,0), handType, handType+intCardValues])

# now I just have to do a quick sort
quickSort(data, 0, len(data) - 1)

# and do the math

winnings = 0
for idx, hand in enumerate(data):
    # index starts with 0
    winnings += hand[1]*(idx+1)

    print(hand[0], hand[2])


# print(data)
print(winnings)


# part 1 250354920 is too high
# part 1 250347426 is right