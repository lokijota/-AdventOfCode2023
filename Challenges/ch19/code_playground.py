import sys
import numpy as np
from collections import Counter
import re
import copy
from tqdm import tqdm
import time
from collections import deque
import random
import anytree
from anytree import NodeMixin, RenderTree, PreOrderIter
import portion # overkill for intervals, probably. but I prefer not to have to write more code / https://github.com/AlexandreDecan/portion

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
    # print("machine_part", machine_part, "has outcome", wf_name, "result= ", result)


print("Result part 1: ", result) # part 1 - 425811
print("--- %s seconds ---" % (time.time() - start_time))

# part 2 - new from apr2024

start_time = time.time()
result = 0

# part A - find all the boundaries

boundaries = {}
boundaries['x'] = []
boundaries['m'] = []
boundaries['a'] = []
boundaries['s'] = []

for wf in workflows:
    for rule in workflows[wf][:-1]:

        # print(rule)
        if rule[1] == '<':
            boundaries[rule[0]].append(rule[2]-1)
            # boundaries[rule[0]].append(rule[2])
        else:
            boundaries[rule[0]].append(rule[2])
            # boundaries[rule[0]].append(rule[2]+1)

for boundary_key in boundaries.keys():
    boundary_list = boundaries[boundary_key]
    # boundary_list.append(1)
    boundary_list.append(4000)

    boundaries[boundary_key] = list(set(boundary_list))
    boundaries[boundary_key].sort()

    print(f"key {boundary_key} - {boundaries[boundary_key]}")


print("squares=", len(boundaries['x'])*len(boundaries['m'])*len(boundaries['a'])*len(boundaries['s']))
#      76.418.241.060 ... this is too much to try 1 by 1
# 256.000.000.000.000 is 4000^4, the total search space, 3350 larger than the reduction above. still too large.
# I think I have to consider only valid squares.


# print(machine_parts)
# part B - have a method to try an individual record
def is_accepted(workflows, machine_part):
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

            if op_result == True: # found a true condition, so go that workflow
                wf_name = rule[3]
                break
        
        if op_result == False: # if we get here with False it's because we ran all the if's -- go to the final workflow"
            wf_name = rules[-1]

    return wf_name == "A"


b = {}
count_accepted = 0
sum_accepted = 0

lastx = 0

# 167409079868000
# 167409079868000
# ok I can reproduce the sample results now in the sample input with the code below

"""
print(len(boundaries['x']))

for xlower in boundaries['x']:
    print(f"x{xlower}")
    b['x'] = xlower
    deltax = xlower - lastx

    start_time = time.time()

    lastm = 0
    for mlower in boundaries['m']:
        b['m'] = mlower
        deltam = mlower - lastm

        lasta = 0
        for alower in boundaries['a']:
            b['a'] = alower
            deltaa = alower - lasta

            lasts = 0
            for slower in boundaries['s']:
                b['s'] = slower

                if is_accepted(workflows, b):
                    # count_accepted += 1
                    deltas = slower - lasts
                    
                    sum_accepted += (deltax*deltam*deltaa*deltas)

                lasts = slower
            lasta = alower
        lastm = mlower
    lastx = xlower

    print("---m %s seconds ---" % (time.time() - start_time))

# print(count_accepted)
print(sum_accepted)


# part C - go over all the combinations (eg the middle point in each) -- create a new list with the middle points!



# result = rating_combinations
# print("Result part 2: ", result)
print("--- %s seconds ---" % (time.time() - start_time))

sys.exit()
"""

# part 2 - old from dec2023

start_time = time.time()
result = 0

# pbar = tqdm(total=4000*4000*4000*4000+1)

# brute force does not work

# 1. build a tree with the connections first

# 1.1 Define node class
class WorkflowNode(NodeMixin):  
    def __init__(self, name, xmas, operator, operand, parent=None, children=None):
        self.name = name
        self.xmas = xmas
        self.operator = operator
        self.operand = operand

        self.parent = parent
        if children:
            self.children = children

# 1.2 For each work/node, create a structure -- top is an exception with "in"
    
root = WorkflowNode("wf", "-", "=", 0)
R_node =  WorkflowNode("R", "-", "=", 0)
A_node =  WorkflowNode("A", "-", "=", 0)

unvisited_workflows = [ ("in", root) ]


while unvisited_workflows:

    wf = unvisited_workflows.pop()

    rules = workflows[wf[0]]

    for rule in rules:
        if type(rule) is list:
            node_name = rule[0] + rule[1] + str(rule[2])
            new_node = WorkflowNode(node_name, rule[0], rule[1], str(rule[2]), parent=wf[1])

            # print(rule)
            if rule[3] not in ["A", "R"]:
                unvisited_workflows.append([rule[3], new_node])
            else:
                end_node = WorkflowNode(rule[3], "-", "=", 0, parent=new_node)

        else: # it's just a wf name or A/R as the "else" clause
            if rule in ["A", "R"]:
                WorkflowNode(rule, "-", "=", 0, wf[1]) # A or R
            else:
                # JOTA - em vez de Else pode ser mais conveniente ter aqui as acções, para n ser preciso ver os siblings? mas posso chamar p os ver, tb.
                else_node = WorkflowNode("else", "-", "=", 0, wf[1]) # A or R
                unvisited_workflows.append([rule, else_node])

                
for pre, _, node in RenderTree(root):
    print("%s%s" % (pre, node.name))

A_nodes = [node for node in PreOrderIter(root, filter_=lambda n: n.name in ('A'))]
# for some_node in A_nodes:
#     print(some_node.name, some_node.parent.name, some_node.is_leaf)


# leaves = [node_i.name for node_i in PreOrderIter(root, filter_=lambda node: node.is_leaf)]
# print(leaves)


# high level algorithm for collecting the data

# start with the leaves that are A nodes
# of each A node, start with 4000*4 and remove bits of this
# when an "else" is found I have to see the siblings to see the restrictions

# JOTA - convenience as we want int intervals / as per docs here: https://github.com/AlexandreDecan/portion
# We want this because of the subtraction in remove_double_counting, or it'd just turn the intervals into open intervals
class IntInterval(portion.AbstractDiscreteInterval):
    _step = 1

Intervalo = portion.create_api(IntInterval)
# End convenient

# for convenience
xmas_to_order = {}
xmas_to_order["x"] = 0
xmas_to_order["m"] = 1
xmas_to_order["a"] = 2
xmas_to_order["s"] = 3


def process_constraint(interval, constraint):
    "Apply a constraint, eg x<1400, to an interval"

    operator = constraint[1]
    operand = int(constraint[2:])

    if operator == "<":
        constraint_interval = Intervalo.closed(0, operand-1)
    else:
        constraint_interval = Intervalo.closed(operand+1, 4000)

    return interval & constraint_interval # intersection

def process_else(xmas_intervals, else_constraints):
    "apply a set of else constraints to an interval. meaning there can be several and they have to be negated/inverted."

    for else_constraint in else_constraints:
        current_interval = xmas_intervals[xmas_to_order[else_constraint[0]]]

        operator = else_constraint[1]
        operand = int(else_constraint[2:])

        if operator == "<": # treat as if it's a ">", eg x<1416 becomes x>1415
            current_interval = process_constraint(current_interval, "_>" + str(operand))
        else: # treat as if it's a ">"
            current_interval = process_constraint(current_interval, "_<" + str(operand))

        xmas_intervals[xmas_to_order[else_constraint[0]]] = current_interval

    return xmas_intervals

def remove_double_counting(processed_intervals, xmas_intervals):
    "If several intervals overlap, then the math doesn't work. and they do. this becomes a geometry hipercube problem"

    print("-------")

    for processed_interval in processed_intervals:
        # there's overlap in all the 4 intervals, so we're double counting
        if processed_interval[0].overlaps(xmas_intervals[0]) and processed_interval[1].overlaps(xmas_intervals[1]) and processed_interval[2].overlaps(xmas_intervals[2]) and processed_interval[3].overlaps(xmas_intervals[3]):

            print()
            print("     :: OVERLAP OF", xmas_intervals[0], xmas_intervals[1], xmas_intervals[2], xmas_intervals[3])
            print("     :: WITH", processed_interval[0], processed_interval[1], processed_interval[2], processed_interval[3])

            xmas_intervals[0] -= processed_interval[0]
            xmas_intervals[0] -= processed_interval[1]
            xmas_intervals[0] -= processed_interval[2]
            xmas_intervals[0] -= processed_interval[3]

            print("     :: RESULTS IN", xmas_intervals[0], xmas_intervals[1], xmas_intervals[2], xmas_intervals[3])
            print()

    # https://stackoverflow.com/questions/28146260/how-to-calculate-the-total-volume-of-multiple-overlapping-parallelepipeds


    for xmi in xmas_intervals:
        if xmi.left == portion.OPEN or xmi.right == portion.OPEN:
            return None

    return [xmas_intervals[0], xmas_intervals[1], xmas_intervals[2], xmas_intervals[3]]

# main code starts here

rating_combinations = 0
processed_intervals = []

for A_node in A_nodes:

    # intervals for x, m, a and s respectively
    xmas_intervals = [Intervalo.closed(1, 4000), Intervalo.closed(1, 4000), Intervalo.closed(1, 4000), Intervalo.closed(1, 4000)]

    A_node = A_node.parent

    while not A_node.is_root:
        print(A_node.name, end=", ")
        
        if A_node.name[0] in ["x", "m", "a", "s"]:
            xmas_intervals[xmas_to_order[A_node.name[0]]] = process_constraint(xmas_intervals[xmas_to_order[A_node.name[0]]], A_node.name)
        elif A_node.name == "else":
            else_conditions = [node.name for node in A_node.siblings]
            xmas_intervals = process_else(xmas_intervals, else_conditions)

        A_node = A_node.parent

    xmas_intervals = remove_double_counting(processed_intervals, xmas_intervals) #or triple or quadrupple or ...

    combinations = 1
    if xmas_intervals is not None:

        for xmas_interval in xmas_intervals:
            combinations *= xmas_interval.upper - xmas_interval.lower+1
            
        processed_intervals.append(xmas_intervals)
    
    print(combinations)

    rating_combinations += combinations

    print(xmas_intervals)
    print()

result = rating_combinations
print("Result part 2: ", result)
print("--- %s seconds ---" % (time.time() - start_time))

# 167409079868000 right on sample
# 496250768000000 mine on sample
# 496534091000000 mine on sample
#  65134731000000


"""
- o meu código seja ele o que estiver a fazer, está a cortar combinações
114188311400004
167409079868000
"""