import numpy as np
import re


# main code

# read all the lines
with open('input.txt') as f:
    lines = f.read().splitlines()

# set limits
# define list of possible games
# read all games
# for each game determine if possible or not

validGames = []
sumValid = 0

for line in lines:
    # Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
    result = re.search("Game (\d+): (.*)", line)
    gameNb = int(result.group(1))

    maxRed = 0
    maxGreen = 0
    maxBlue = 0

    plays = result.group(2).split(";")

    for play in plays:
        extractions = play.strip().split(',')

        for extraction in extractions:
            extractionParts = extraction.strip().split(' ')

            nbBlocks = int(extractionParts[0])
            blockColor = extractionParts[1]

            if blockColor == 'red':
                if nbBlocks > maxRed:
                    maxRed = nbBlocks
            elif blockColor == 'green':
                if nbBlocks > maxGreen:
                    maxGreen = nbBlocks
            elif blockColor == 'blue':
                if nbBlocks > maxBlue:
                    maxBlue = nbBlocks

    print("Game ", gameNb, maxRed, maxGreen, maxBlue)

    # check if game is possible
    if maxRed <= 12 and maxGreen <= 13 and maxBlue <= 14:
        validGames.append(gameNb)
        sumValid += gameNb

print(validGames)
print("Sum=", sumValid)

# part 1 - 2795
