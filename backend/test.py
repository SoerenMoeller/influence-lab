import model.problem_data as pbd
import model.points as pts
from model.solver import Solver
from model.points import Point
from src.solver.solve import solve
from data.problems import get_problems


def main():
    problem_data = get_problems()[0]
    solver_type = Solver.UNINTEPRETED_FUNCTIONS
    points = solve(problem_data, solver_type)['points']

    for a in points:
        for b in points[a]:
            print(f'{(a, b)}:')
            print(points[a][b])
    print()
    
    print('Compositions: ')
    print(pts.compose_points(points['a']['b'], points['b']['d']))
    print(pts.compose_points(points['a']['c'], points['c']['d']))
    
    # points = {
    #     'a': {
    #         'c': [Point(x=0, y=0.08333333333333333), Point(x=0.9166666666666666, y=0.08333333333333333), Point(x=1.0, y=1.0833333333333333)],
    #         'b': [Point(x=0, y=0.9166666666666666), Point(x=0.9166666666666666, y=0.9166666666666666), Point(x=1.0, y=0.75)]
    #     },
    #     'c': {
    #         'd': [Point(x=0, y=0.5), Point(x=0.08333333333333333, y=0.5), Point(x=0.16666666666666666, y=0.5833333333333334), Point(x=1.0833333333333333, y=0.5833333333333334), Point(x=2.0, y=0.5833333333333334)]
    #     },
    #     'b': {
    #         'd': [Point(x=0, y=0.0), Point(x=0.75, y=0.5833333333333334), Point(x=0.8333333333333334, y=0.5833333333333334), Point(x=0.9166666666666666, y=0.5833333333333334), Point(x=1.0, y=0.5833333333333334), Point(x=2.0, y=0.6666666666666666)]
    #     } 
    # }

    # ('a', 'd')
    # [Point(x=0, y=0.5), Point(x=0.9166666666666666, y=0.5), Point(x=0.923611111111111, y=0.5833333333333334), Point(x=1.0, y=0.5833333333333334)]
    
    # points = pts.build_composition_points(problem_data, points)
    # for a in points:
    #     for b in points[a]:
    #         print(f'{(a, b)}:')
    #         print(points[a][b])



if __name__ == '__main__':
    main()