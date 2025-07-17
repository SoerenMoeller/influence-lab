import model.problem_data as pbd
import model.points as pts
from model.solver import Solver
from model.points import Point
from src.solver.solve import solve
from data.problems import get_problems


def main():
    problem_data = get_problems()[0]
    solver_type = Solver.SAT
    result = solve(problem_data, solver_type)
    
    if not result['result']:
        print('No solution found')
        return
    
    points = result['points']
    for a in points:
        for b in points[a]:
            print(f'{(a, b)}:')
            print(points[a][b])


if __name__ == '__main__':
    main()