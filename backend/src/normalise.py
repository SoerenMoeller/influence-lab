from model.interval import Interval
from model.scheme import Scheme
from model.statement import Statement
from model.problem_data import ProblemData
import src.poi as poi
import src.rules as rules


def normalise(problem_data: ProblemData) -> ProblemData:
    problem_data.scheme.statements = {
        (a, b): normalise_subscheme(problem_data, a, b)
        for (a, b) in problem_data.scheme.statements
    } 
    return problem_data


def normalise_subscheme(problem_data: ProblemData, var_from: str, var_to: str) -> list[Statement]:
    statements = problem_data.scheme.statements[(var_from, var_to)]
    transforms = [overlap_free, minimal_height] 

    for fn in transforms: 
        statements = fn(problem_data, var_from, statements)

    return statements


def overlap_free(problem_data: ProblemData, var_from: str, statements: list[Statement]) -> list[Statement]:
    bounds = poi.boundaries(problem_data, var_from)
    
    result = []
    for i in range(len(bounds) - 1):
        x = bounds[i] 
        y = bounds[i + 1]
    
        overlapping = rules.overlapping(statements, Interval(x, y))
        st = rules.intersect(overlapping, Interval(x, y))
        
        if result is not None:
            result.append(st)

    return result


def minimal_height(problem_data: ProblemData, var_from: str, sts: list[Statement]) -> list[Statement]:
    i = 0
    while 0 <= i < len(sts) - 1:
        go_left = False 
        
        assert sts[i].domain.end == sts[i + 1].domain.start, \
            'Gap found while normalising'

        new_st = rules.left_rule(sts[i], sts[i + 1])
        if new_st is not None:
            go_left = True 
            sts[i] = new_st
            
        new_st = rules.right_rule(sts[i], sts[i + 1])
        if new_st is not None:
            go_left = True 
            sts[i + 1] = new_st
            
        if go_left:
            i -= 1
        else:
            i += 1 
        
    return sts