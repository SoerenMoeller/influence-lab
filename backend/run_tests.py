from collections import namedtuple    
from model.solver import Solver
import data.flat as flat
import src.solver.solve as solve_module


Benchmark = namedtuple('Benchmark', ['name', 'get_problem', 'problem_args'])


BENCHMARKS = [
    Benchmark(
        name="Flat Scheme",
        get_problem=lambda x, y: flat.get_problem(x, y),
        problem_args=[(x, 2) for x in [1, 10, 20, 50, 100]]
    ),
    Benchmark(
        name="Flat Scheme",
        get_problem=lambda x, y: flat.get_problem(x, y),
        problem_args=[(x, 2) for x in [1, 10, 20, 50, 100]]
    ),
]


SOLVERS = [
    # Solver.SAT, 
    Solver.UNINTEPRETED_FUNCTIONS, 
    # Solver.ARRAY, 
    Solver.INTEGER, 
    Solver.INCREMENTAL
]


def main():
    for solver_type in SOLVERS:
        print(f"========== Testing solver type: {solver_type} ==========")
        test_solver_type(solver_type)
        print()
    

def test_solver_type(solver_type: Solver):
    for bm in BENCHMARKS:
        print(f"---- Benchmark: {bm.name} ----")
        for args in bm.problem_args:
            print(f"- {args}")
            problem = bm.get_problem(*args)
            solve_module.solve(problem, solver_type)


if __name__ == "__main__":
    main()
    
