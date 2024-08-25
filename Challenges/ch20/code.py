import sys
import numpy as np
from collections import Counter
import re
import copy
from tqdm import tqdm
import time
from collections import deque
import random
# import anytree
# from anytree import NodeMixin, RenderTree, PreOrderIter

# functions

# main code

# read all the lines
with open('Challenges/ch20/sample.txt') as f:
    lines = f.read().splitlines()

# broadcaster -> a, b, c
# %a -> b
# %b -> c
# %c -> inv
# &inv -> a


# parse data file content
modules = {}

for line in lines:
    parts = line.split(" -> ")

    destinations = parts[1].split(", ")

    if parts[0].startswith("%"):
        new_module = ["%", np.zeros(1, dtype=int), destinations]
        module_name = parts[0][1:]

    elif parts[0].startswith("&"):
        new_module = ["%",  np.zeros(len(destinations), dtype=int), destinations]
        module_name = parts[0][1:]

    else: # broadcaster
        new_module = ["B",  0, destinations]
        module_name = parts[0]

    modules[module_name] = new_module        


print(modules)


# workflows = {}
# machine_parts = []

# for line in lines:
#     if len(line) == 0:
#         parsing_workflow = False
#         continue

#     if parsing_workflow:
#         # px{a<2006:qkq,m>2090:A,rfg}
#         parts = line.split("{")

#         wf_name = parts[0]
#         rule_parts = parts[1].removesuffix("}").split(",")
#         rules = [[rule[0], rule[1],int(rule.split(":")[0][2:]), rule.split(":")[1]] for rule in rule_parts[:-1]]
#         rules.append(rule_parts[-1])

#         workflows[wf_name] = rules
#         # print(wf_name, rules)

#     else: #parsing variable names - {x=787,m=2655,a=1222,s=2876}
#         parts = line.removeprefix("{").removesuffix("}").split(",")
        
#         auxdict = {}
#         for part in parts:
#             auxdict[part[0][0]] = int(part.split("=")[1])

#         machine_parts.append(auxdict)

# global variables
result = 0

# process data

# part 1
start_time = time.time()

print("Result part 1: ", result) # part 1 - 425811
print("--- %s seconds ---" % (time.time() - start_time))

# part 2 - new from apr2024

start_time = time.time()
result = 0


print("Result part 2: ", result) # part 1 - 425811
print("--- %s seconds ---" % (time.time() - start_time))