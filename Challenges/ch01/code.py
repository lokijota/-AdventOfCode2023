import numpy as np

def findFirstDigit(str):
    pos = []
    pos.append(str.find("one"))
    pos.append(str.find("two"))
    pos.append(str.find("three"))
    pos.append(str.find("four"))
    pos.append(str.find("five"))
    pos.append(str.find("six"))
    pos.append(str.find("seven"))
    pos.append(str.find("eight"))
    pos.append(str.find("nine"))
    pos.append(str.find("1"))
    pos.append(str.find("2"))
    pos.append(str.find("3"))
    pos.append(str.find("4"))
    pos.append(str.find("5"))
    pos.append(str.find("6"))
    pos.append(str.find("7"))
    pos.append(str.find("8"))
    pos.append(str.find("9"))

    pos = [10000 if digitpos == -1 else digitpos for digitpos in pos]

    mindigit = min(pos)
    mindigitpos = pos.index(mindigit)

    if mindigitpos < 9:
        return mindigitpos + 1
    else:
        return mindigitpos - 9 +1

def findLastDigit(str):
    pos = []
    pos.append(str.rfind("one"))
    pos.append(str.rfind("two"))
    pos.append(str.rfind("three"))
    pos.append(str.rfind("four"))
    pos.append(str.rfind("five"))
    pos.append(str.rfind("six"))
    pos.append(str.rfind("seven"))
    pos.append(str.rfind("eight"))
    pos.append(str.rfind("nine"))
    pos.append(str.rfind("1"))
    pos.append(str.rfind("2"))
    pos.append(str.rfind("3"))
    pos.append(str.rfind("4"))
    pos.append(str.rfind("5"))
    pos.append(str.rfind("6"))
    pos.append(str.rfind("7"))
    pos.append(str.rfind("8"))
    pos.append(str.rfind("9"))

    maxdigit = max(pos)
    maxdigitpos = pos.index(maxdigit)

    if maxdigitpos < 9:
        return maxdigitpos + 1
    else:
        return maxdigitpos - 9 +1
    

# main code

# read all the lines
with open('input.txt') as f:
    lines = f.read().splitlines()

# part one
# sum = 0
# for line in lines:
#     digits = re.findall(r'[0-9]+', line)
#     firstdigit = digits[0][0]
#     lastdigits = digits[len(digits)-1]
#     lastdigit = lastdigits[len(lastdigits)-1]

#     str = firstdigit + lastdigit
#     # print(digits)

#     sum += int(str)

# print("Part 1 solution is", sum)

# part two

sum = 0
for line in lines:
    digits = str(findFirstDigit(line)) + str(findLastDigit(line))
    sum += int(digits)


print("Part 2 solution is", sum)

# 52155 is too low
# 52851 is too high
# 52844 is too high
# 52840