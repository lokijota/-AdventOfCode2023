import numpy as np
from collections import Counter
import re
import copy
from tqdm import tqdm
import time
from collections import deque
import random
import sys
import json


# functions

# main code

# read all the lines
with open('Challenges/ch19/input.txt') as f:
    lines = f.read().splitlines()

# parse data file content

parsing_workflow = True

workflows = {}
machine_parts = []

for line in lines:
    if len(line) == 0:
        parsing_workflow = False
        continue

    if parsing_workflow:
        # px{a<2006:qkq,m>2090:A,rfg}
        parts = line.split("{")

        wf_name = parts[0]
        rule_parts = parts[1].removesuffix("}").split(",")
        rules = [[rule[0], rule[1],int(rule.split(":")[0][2:]), rule.split(":")[1]] for rule in rule_parts[:-1]]
        rules.append(rule_parts[-1])

        workflows[wf_name] = rules
        # print(wf_name, rules)

    else: #parsing variable names - {x=787,m=2655,a=1222,s=2876}
        parts = line.removeprefix("{").removesuffix("}").split(",")
        
        auxdict = {}
        for part in parts:
            auxdict[part[0][0]] = int(part.split("=")[1])

        machine_parts.append(auxdict)

# print(workflows)
# print(machine_parts)

# global variables

# process data

# part 1
start_time = time.time()
result = 0

for machine_part in machine_parts:
    wf_name = "in"

    while wf_name != "A" and wf_name!="R":
        rules = workflows[wf_name]
        op_result = False

        for rule in rules[:-1]:
            left_operand = machine_part[rule[0]]
            operand = rule[1]
            right_operand = rule[2]

            if operand == "<":
                op_result = left_operand < right_operand
            else:
                op_result = left_operand > right_operand

            if op_result == True:
                wf_name = rule[3]
                break
        
        if op_result == False:
            wf_name = rules[-1]

    if wf_name == "A":
        result += sum(machine_part.values())
    print("machine_part", machine_part, "has outcome", wf_name, "result= ", result)
    


        # 'px': [['a', '<', 2006, 'qkq'], ['m', '>', 2090, 'A'], 'rfg']


print("Result part 1: ", result) # part 1 - 425811
print("--- %s seconds ---" % (time.time() - start_time))

# part 2

start_time = time.time()
result = 0

print("Result part 2: ", result)
print("--- %s seconds ---" % (time.time() - start_time))
