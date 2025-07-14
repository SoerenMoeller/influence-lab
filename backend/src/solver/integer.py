from z3 import *

# # Points of interest:
# points = [0, 1, 2, 3, 4]

# # Variables for function outputs:
# f_ab = {x: Int(f'f_ab_{x}') for x in points}
# f_bc = {y: Int(f'f_bc_{y}') for y in points}
# f_ac = {x: Int(f'f_ac_{x}') for x in points}

# solver = Solver()

# # Composition constraints:
# for x in points:
#     solver.add(f_ac[x] == f_bc[f_ab[x]])  # Composition

# # Example:
# solver.add(f_ab[0] == 2)
# solver.add(f_bc[2] == 3)
# solver.add(f_ac[0] != 3)  # Should be UNSAT

# print(solver.check())