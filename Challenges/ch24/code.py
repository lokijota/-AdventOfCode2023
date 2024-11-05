import time
from collections import deque
import sys
import numpy as np
from collections import Counter
import re
import copy
from tqdm import tqdm
import random
import matplotlib.pyplot as plt
import numpy as np
from sympy import solve, Eq, linsolve, Symbol
from sympy.parsing.sympy_parser import parse_expr
from sympy.abc import t,x,y

# functions

# main code

# read all the lines
with open('Challenges/ch24/input.txt') as f:
    lines = f.read().splitlines()

hailstones = []
for line in lines:
    result = re.search("(\d+),\s(\d+),\s(\d+)\s@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)", line)
    hailstone = (int(result.group(1)), int(result.group(2)), int(result.group(3)), int(result.group(4)), int(result.group(5)), int(result.group(6)))
    hailstones.append(hailstone)

# print(hailstones)

# global variables

# process data

## part 1
start_time = time.time()
result = 0

print("--------")

# print("*** Equation 1 ***")
# 01. core movement equations (first equation)
eq_x = 19-2*t-x
eq_y = 13+t-y

# 02. solve for t, so that t=...
t_on_x = solve(eq_x, t, dict=True)
t_on_y = solve(eq_y, t, dict=True)
# print("t(x)= ", t_on_x[0][t], "\n t(y):", t_on_y[0][t])

# 03. by making them equal we have the equation of the line
line_eq1 = Eq(t_on_x[0][t], t_on_y[0][t])
# print("Equation of the line: ", line_eq1)

# now do the same for the second line

# print("\n*** Equation 2 ***")
# 01. core movement equations (second equation)
eq_x2 = 18-t-x
eq_y2 = 19-t-y

# 02. solve for t, so that t=...
t_on_x = solve(eq_x2, t, dict=True)
t_on_y = solve(eq_y2, t, dict=True)

# 03. by making them equal we have the equation of the line
line_eq2 = Eq(t_on_x[0][t], t_on_y[0][t])

# print("line_eq1:", line_eq1)
# print("line_eq2:", line_eq2)
print(linsolve([line_eq1, line_eq2], (x,y)))

print("---***---")

# Hailstone A: 19, 13 @ -2, 1
x = 19 + -2*t
y = 13 + t

# Hailstone B: 18, 19 @ -1, -1
# Hailstones' paths will cross inside the test area (at x=14.333, y=15.333).
x = 18 - t
y = 19 - t

## 01. For each equation create the equation of the line

lines = []

print("Creation equations of the line, for each equation...")
for hailstone in hailstones:
	# movement equations
	eq_x = parse_expr(f"{hailstone[0]} + {hailstone[3]}*t -x")
	eq_y = parse_expr(f"{hailstone[1]} + {hailstone[4]}*t -y")

	# solve for t, so that t=...
	t_eq_x = solve(eq_x, t, dict=True)
	t_eq_y = solve(eq_y, t, dict=True)	
     
	# by making them equal of have the equation of the line
	line_eq = Eq(t_eq_x[0][t], t_eq_y[0][t])

	# print("Line Equation: ", line_eq)
     
	# Add the line equation to the list, and also the time equations (only one is needed, hence x), to check if the solution is in the past, later on
	lines.append((line_eq, t_eq_x[0][t]))

## 02. Now try all the combinations and solve the equations

min_boundary = 200000000000000
max_boundary = 400000000000000
result = 0

queue = lines
results = []

print("Try all the combinations and solve the equations")
while len(queue) > 0:
	le1 = queue[0]
	queue = queue[1:]     

	# try to solve the head equation vs all the remaining ones in the queue
	for le2 in queue:

		# need to call this to reset x/y or it won't solve equations
		x=Symbol('x')
		y=Symbol('y')

		sol = linsolve([le1[0], le2[0]], (x,y))
		if len(sol) > 0:
			# if there is a solution
			sol_x = sol.args[0][0]
			sol_y = sol.args[0][1]

			# check if the solution is in the boundaries for the problem
			if sol_x >= min_boundary and sol_x <= max_boundary and sol_y >= min_boundary and sol_y <= max_boundary:

				# print(le1[1].subs(x, sol_x), " / ",  le2[1].subs(x, sol_x))
				# if I remember correctly from all the way back just two weeks ago, this is to check if the cross is in the future for both lines
				if le1[1].subs(x, sol_x) >= 0 and le2[1].subs(x, sol_x) >= 0:
					result += 1
					# print(".", end="")
					# print("Sol in Square: ", sol_x, sol_y)

print(f"Result part 1: {result}")
print("--- %s seconds ---" % (time.time() - start_time))

# Result part 1: 11995
# --- 10.869709253311157 seconds ---

## part 2 

# https://math.stackexchange.com/questions/607348/line-intersecting-three-or-four-given-lines
# Your GeoGebra project helped me to better understand the structure of the problem and that 4 trajectories are sufficient to find the solution" 
# pg143/299 https://upload.wikimedia.org/wikipedia/commons/5/54/Analytic_geometry_of_space_%28IA_analygeomspace00snydrich%29.pdf 
# https://www.quora.com/Given-four-skew-lines-how-many-lines-intersect-all-of-them

# input("*********** Press Enter to continue... **********")
# start_time = time.time()
# print("Result part 2: ", result) #
# print("--- %s seconds ---" % (time.time() - start_time))

