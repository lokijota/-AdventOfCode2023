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
        # TODO: tenho de inicializar com o numero de origens e não com o número de destinos
        new_module = ["&",  0 , destinations, {}] #np.zeros(len(destinations), dtype=int)
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

# process data

def queue_signal(target, signal, source):
    signal_queue.append([target, signal, source])
    count[signal] += 1

def queue_signals(targets, signal, source):
    for target in targets:
        queue_signal(target, signal, source)

# part 1
start_time = time.time()

# button presses loop

for pressn in range(1000):

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

print("Result part 1: ", result) # part 1 - 
print("--- %s seconds ---" % (time.time() - start_time))

# part 2 - new from apr2024

start_time = time.time()
result = 0


print("Result part 2: ", result) # part 1 - 425811
print("--- %s seconds ---" % (time.time() - start_time))