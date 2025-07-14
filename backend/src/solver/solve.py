from typing import Optional
from model.points import Points
from model.problem_data import ProblemData
from model.solver import Solver


import src.solver.sat as sat_solver
import src.solver.uninterpreted as unintepreted_solver


def solve(problem_data: ProblemData, solver_type: Solver) -> dict:
    solve_fn_mapping = {
        Solver.SAT: _solve_sat,
        Solver.UNINTEPRETED_FUNCTIONS: _solve_uninterpreted
    } 
    
    solve_fn = solve_fn_mapping[solver_type]
    points = solve_fn(problem_data)
    
    if points is None:
        return {
            'result': False
        }
        
    return {
        'result': True,
        'points': points    
    }
    

def _solve_sat(problem_data: ProblemData) -> Optional[Points]:
    sat_solver.build_formula(problem_data, 'sat-formula')
    model = sat_solver.solve('sat-formula')

    if not model:
        return None
    
    return sat_solver.extract_model(problem_data, model)
    
    
def _solve_uninterpreted(problem_data: ProblemData) -> Points:
    ...    
    