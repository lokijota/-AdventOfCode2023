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
from sympy import solve, Eq, linsolve, symbols, nonlinsolve
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

#  variables

# process data

## part 2
start_time = time.time()
result = 0

print("-------- Trying out the Api of SympPy --------")

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
equations = []

px, py, pz = symbols("px, py, pz")
vx, vy, vz = symbols("vx, vy, vz")
t0, t1, t2, t3 = symbols("t0, t1, t2, t3")

print("Creation equations of the line, for the four first lines...")
for idx, hailstone in enumerate(hailstones[:3]):

	# generate an equation for the line we're trying to find
	target_x = parse_expr(f"px + vx * t{idx}")
	target_y = parse_expr(f"py + vy * t{idx}")
	target_z = parse_expr(f"pz + vz * t{idx}")

	# movement equations for each hailstone
	hailstone_eq_x = parse_expr(f"{hailstone[0]} + {hailstone[3]}*t{idx}")
	hailstone_eq_y = parse_expr(f"{hailstone[1]} + {hailstone[4]}*t{idx}")
	hailstone_eq_z = parse_expr(f"{hailstone[2]} + {hailstone[5]}*t{idx}")

	# now make them equal in the right dimention
	intersection_x = Eq(target_x, hailstone_eq_x)
	intersection_y = Eq(target_y, hailstone_eq_y)
	intersection_z = Eq(target_z, hailstone_eq_z)

	print(intersection_x)
	print(intersection_y)
	print(intersection_z)
	print()
	equations.append(intersection_x)
	equations.append(intersection_y)
	equations.append(intersection_z)

# Now try to solve the equations. We should have 3*3 (9) equalities and 3 time variables plus 3 position variables (posx, posy, posz)
# and 3 velocity variables (9 variables in total) - 9 variáveis e 9 incógnitas


# have to use nonlinsolve due to the v*t multiplication https://docs.sympy.org/latest/modules/solvers/solvers.html
sol = nonlinsolve(equations, (px, py, pz, vx, vy, vz, t0, t1, t2))
if len(sol) > 0:
	print(f">>>>> Solution: {sol}")
	result = sol.args[0][0]+sol.args[0][1]+sol.args[0][2] 
else:
	print(">>>>> No solution, upsie")

# Solution = 

print(f"Result part 1: {result}")
print("--- %s seconds ---" % (time.time() - start_time))

# Result part 2: 983620716335751
# --- 0.19272398948669434 seconds seconds ---

