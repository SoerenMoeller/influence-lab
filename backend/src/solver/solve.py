from typing import Optional
from model.points import Points
from model.problem_data import ProblemData
from model.solver import Solver


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
    points = solve_module.solve(problem_data)

    if points is None:
        return {
            'result': False
        }
        
    points = pts.build_composition_points(problem_data, points)
    return {
        'result': True,
        'points': points    
    }
