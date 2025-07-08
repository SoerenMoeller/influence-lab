import sys


import src.io as io
import src.points as points
import model.variable as vbl
import src.solver.sat as solver
from model.scheme import Scheme
from scheme import schemes
import json


def main() -> int:
    # args = sys.argv[1]
    # statements = io.json_to_statement_list(args)
    # scheme = Scheme(statements)
    scheme = schemes[0]
    solver.build_formula(scheme, 'sat-formula')
    model = solver.solve('sat-formula')
    
    if not model:
        return 1
    
    result = solver.extract_model(scheme, model)
    print('<<<RESULT>>>')
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    main()
