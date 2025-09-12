from collections import namedtuple    
from model.solver import Solver
import data.flat as flat
import data.comp as comp
import src.solver.solve as solve_module


Benchmark = namedtuple('Benchmark', ['name', 'get_problem', 'problem_args', 'active'])


BENCHMARKS = [
    Benchmark(
        name="Flat Scheme",
        get_problem=lambda x, y: flat.get_problem(x, y),
        problem_args=[(x, 2) for x in [1, 10, 20, 50, 100]],
        active=False
    ),
    Benchmark(
        name="Composition Chains",
        get_problem=comp.get_problem,
        problem_args=[(20, 1.5, 3, x) for x in [2, 6, 10, 14, 18, 22]],
        active=True
    ),
]


SOLVERS = [
    # Solver.SAT, 
    # Solver.UNINTEPRETED_FUNCTIONS, 
    # Solver.ARRAY, 
    Solver.INTEGER, 
    # Solver.INCREMENTAL
]


def main():
    for solver_type in SOLVERS:
        print(f"========== Testing solver type: {solver_type.value} ==========")
        test_solver_type(solver_type)
        print()
    

def test_solver_type(solver_type: Solver):
    for bm in BENCHMARKS:
        if not bm.active:
            continue
        
        print(f"---- Benchmark: {bm.name} ----")
        for args in bm.problem_args:
            print(f"- {args}")
            problem = bm.get_problem(*args)
            solve_module.solve(problem, solver_type)


if __name__ == "__main__":
    main()
    
