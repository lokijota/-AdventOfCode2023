import sys
import numpy as np
from collections import Counter
import re
import copy
from tqdm import tqdm
import time
from collections import deque
import random

# functions

# main code

# read all the lines
with open('Challenges/ch20/input.txt') as f:
    lines = f.read().splitlines()

# parse data file content
modules = {}
set_sources = set()
set_destinations = set()

for line in lines:
    parts = line.split(" -> ")

    destinations = parts[1].split(", ")

    if parts[0].startswith("%"):
        new_module = ["%", 0, destinations]
        module_name = parts[0][1:]

    elif parts[0].startswith("&"):
        new_module = ["&",  0 , destinations, {}]
        module_name = parts[0][1:]

    else: # broadcaster
        new_module = ["B",  0, destinations]
        module_name = parts[0]

    set_sources.add(module_name)
    for destination in destinations:
        set_destinations.add(destination)

    modules[module_name] = new_module        

# check if there are elements that are in one set and not others (eg, "output")
for sink_module in set_destinations-set_sources:
    modules[sink_module] = ["S", 0, []]

# post-process: auxiliary structure for the nand
nand_modules_inputs = {}
for module_name, module_config in modules.items():

    for target_module_name in module_config[2]:

        if modules[target_module_name][0] == "&":

            if target_module_name not in nand_modules_inputs.keys():
                nand_modules_inputs[target_module_name] = [module_name]
            else:
                nand_modules_inputs[target_module_name].append(module_name)


# print(nand_modules_inputs)
# e.g., {'inv': ['a'], 'con': ['a', 'b']}
                
# {'broadcaster': ['B', 0, ['a']],
#  'a': ['%', 0, ['inv', 'con']],
#  'inv': ['&', array([0]), ['b'], {'a': 0}],
#  'b': ['%', 0, ['con']],
#  'con': ['&', array([0, 0]), ['output'], {'a': 0, 'b': 1}],
#  'output': ['S', 0, []]}

# now that we have this auxiliary structure, let's go over the modules and update the &'s
for nand_key, nand_origins in nand_modules_inputs.items():
    module = modules[nand_key]
    module[1] = np.zeros(len(nand_origins), dtype=int)
    module[3] = {}
    order = 0
    for nand_origin in nand_origins:
        module[3][nand_origin] = order
        order += 1

# print(modules)

# global variables
result = 0
signal_queue = deque()
count = np.zeros(2, dtype=int)
total_button_presses = 0

# process data

def queue_signal(target, signal, source):
    signal_queue.append([target, signal, source])
    count[signal] += 1

    # if(target == "rx" and signal == 0):
    #     print(f"Got a 0 in rx after {total_button_presses}")

def queue_signals(targets, signal, source):
    for target in targets:
        queue_signal(target, signal, source)

# part 1
start_time = time.time()

# button presses loop

for pressn in range(-1): #1000 - using -1 to skip

    queue_signal("broadcaster", 0, "button")

    while len(signal_queue) > 0:
        sig = signal_queue.popleft()
        # print(sig)

        if sig[0] == "broadcaster":
            queue_signals(modules[sig[0]][2], 0, sig[0])
        else:
            # get the module that's receiving the signal
            target_module = modules[sig[0]]
            if target_module[0] == "%": #flip-flop
                if sig[1] == 0:
                    # we must flip
                    target_module[1] = (target_module[1] + 1) % 2
                    # and send it to all connected modules
                    queue_signals(target_module[2], target_module[1], sig[0])
            elif target_module[0] == "&": #nand
                # 1. update the position of the received signal
                position_to_update = target_module[3][sig[2]]
                target_module[1][position_to_update] = sig[1]

                # 2. check if all of them are 1, send a 0 / else send a 1
                if sum(target_module[1]) == len(target_module[3]):
                    queue_signals(target_module[2], 0, sig[0])
                else:
                    queue_signals(target_module[2], 1, sig[0])

# print(count)

result = count[0] * count[1]

print(count)
print("Result part 1: ", result) # part 1 - 
print("--- %s seconds ---" % (time.time() - start_time))

# part 2 - new from apr2024

# input("*********** Press Enter to continue... **********")

start_time = time.time()
postions_of_zero = {}
postions_of_zero["ks"] = 0
postions_of_zero["sx"] = 0
postions_of_zero["jt"] = 0
postions_of_zero["kb"] = 0
count_finds = 0

# not needed
# def principal_period(s):
#     i = (s+s).find(s, 1, -1)
#     return None if i == -1 else s[:i]

while total_button_presses < 2000000: #True:

    queue_signal("broadcaster", 0, "button")
    total_button_presses += 1

    while len(signal_queue) > 0:
        sig = signal_queue.popleft()

        if sig[0] == "broadcaster":
            queue_signals(modules[sig[0]][2], 0, sig[0])
        else:
            # get the module that's receiving the signal
            target_module = modules[sig[0]]
            if target_module[0] == "%": #flip-flop
                if sig[1] == 0:
                    # we must flip
                    target_module[1] = (target_module[1] + 1) % 2
                    # and send it to all connected modules
                    queue_signals(target_module[2], target_module[1], sig[0])
            elif target_module[0] == "&": #nand
                # 1. update the position of the received signal
                position_to_update = target_module[3][sig[2]]
                target_module[1][position_to_update] = sig[1]


                # I sketched the network on paper and got that rx received from zh which received from the next four in the list.
                # I did some debugs and they mostly output 1. Below I am just looking for the first 0 from each of them, 
                # and assume that the pattern repeats and a 0 shows up every N elements, with a different N for each of the
                # four modules that lead to zh. So if that's the periodicity, I just find it and multiply them together to find the
                # minimum common denominator, the place they all meet.
                # Not a generic solution, I don't like that (as the repeating sequence could have more elements after the zero). 
                # But it works and it's fast.s
                if sig[0] in ["ks", "sx", "jt", "kb"]:

                    if sig[1] == 0 and postions_of_zero[sig[0]] == 0:
                        postions_of_zero[sig[0]] = total_button_presses
                        print(f"{sig[0]} was 1 at position {total_button_presses}")
                        count_finds += 1
                        if count_finds == 4:
                            result = 1
                            for el in postions_of_zero.values():
                                result *= el

                            print("Result part 2: ", result) # 
                            print("--- %s seconds ---" % (time.time() - start_time))
                            exit()
                        
                # 2. check if all of them are 1, send a 0 / else send a 1
                if sum(target_module[1]) == len(target_module[3]):
                    queue_signals(target_module[2], 0, sig[0])
                else:
                    queue_signals(target_module[2], 1, sig[0])
