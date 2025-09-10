from typing import Optional
from model.points import Points
from model.problem_data import ProblemData
from model.solver import Solver
import time


import model.points as pts
import src.solver.sat as sat_solver
import src.solver.uninterpreted as unintepreted_solver
import src.solver.array as array_solver
import src.solver.integer as integer_solver
import src.solver.incremental as incremental_solver


def solve(problem_data: ProblemData, solver_type: Solver) -> dict:
    solver_modules = {
        Solver.SAT: sat_solver,
        Solver.UNINTEPRETED_FUNCTIONS: unintepreted_solver,
        Solver.ARRAY: array_solver,
        Solver.INTEGER: integer_solver,
        Solver.INCREMENTAL: incremental_solver,
    } 
    
    solve_module = solver_modules[solver_type]
    start_time = time.time()
    solve = solve_module.build_formula(problem_data) 
    print( f"Build time: {time.time() - start_time:.2f}s")
    start_time = time.time()
    points = solve()
    print( f"Solve time: {time.time() - start_time:.2f}s")

    if points is None:
        return {
            'result': False
        }
        
    points = pts.build_composition_points(problem_data, points)
    return {
        'result': True,
        'points': points    
    }
