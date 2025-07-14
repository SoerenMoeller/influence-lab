import sys
from z3 import *


from model.behaviour import Behaviour
import src.io as io
import src.points as points
import model.variable as vbl
import src.solver.sat as solver
from model.scheme import Scheme
from scheme import schemes
import json



def main() -> int:
    args = sys.argv[1]
    problem_data  = schemes[0]
    solver.build_formula(problem_data, 'sat-formula')
    model = solver.solve('sat-formula')

    if not model:
        return 1
    
    result = solver.extract_model(problem_data, model)
    print('<<<RESULT>>>')
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    main()
