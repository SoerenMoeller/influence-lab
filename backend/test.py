from collections import defaultdict
import json
import src.solver.uninterpreted as solver
import model.variable as vbl
from scheme import schemes

def main():
    problem_data = schemes[0]
    result: dict[str, dict[str, list]] = solver.solve(problem_data)
    
    if not result:
        return 1
    
    # print('<<<RESULT>>>')
    # print(json.dumps(result))

    print(result)
    scheme = problem_data.scheme
    
    experiment = defaultdict(lambda: defaultdict(list))
    for a in scheme.variables:
        for b in vbl.post(scheme, a):
            experiment[a][b] = result[a][b]
            
    print(experiment)

    var_queue = [var for var in scheme.variables if vbl.is_minimal(scheme, var)]
    while var_queue:
        var = var_queue[0]
        var_queue = var_queue[1:]
        print(var, vbl.post(scheme, var))
    print(var_queue)
    
    return 0
    
if __name__ == '__main__':
    main()