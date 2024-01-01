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


# functions

# main code

# read all the lines
with open('Challenges/ch19/sample.txt') as f:
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

# part 2

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
for some_node in A_nodes:
    print(some_node.name, some_node.parent.name, some_node.is_leaf)


leaves = [node_i.name for node_i in PreOrderIter(root, filter_=lambda node: node.is_leaf)]
print(leaves)

# branches = [[node_i.name for node_i in data_i.path] for data_i in PreOrderIter(f, filter_=lambda node: node.is_leaf)]

# print(RenderTree(root, style=ContStyle()))

# for x in range(1, 4001):
#     for m in range(1, 4001):
#        for a in range(1, 4001):
#            for s in range(1, 4001):

#                 wf_name = "in"

#                 while wf_name != "A" and wf_name!="R":
#                     rules = workflows[wf_name]
#                     op_result = False

#                     for rule in rules[:-1]:
#                         left_operand = machine_part[rule[0]]
#                         operand = rule[1]
#                         right_operand = rule[2]

#                         if operand == "<":
#                             op_result = left_operand < right_operand
#                         else:
#                             op_result = left_operand > right_operand

#                         if op_result == True:
#                             wf_name = rule[3]
#                             break
                    
#                     if op_result == False:
#                         wf_name = rules[-1]

#                 if wf_name == "A":
#                     result += 1

                # pbar.update(1)

# pbar.close()

print("Result part 2: ", result)
print("--- %s seconds ---" % (time.time() - start_time))
