from model.interval import Interval
from model.scheme import Scheme
from model.statement import Statement
import src.points as points
import src.rules as rules


def normalise(scheme: Scheme) -> Scheme:
    scheme.statements = {
        (a, b): normalise_subscheme(scheme, a, b)
        for (a, b) in scheme.statements
    } 
    return scheme


def normalise_subscheme(scheme: Scheme, var_from: str, var_to: str) -> list[Statement]:
    statements = scheme.statements[(var_from, var_to)]
    transforms = [overlap_free, minimal_height] 

    for fn in transforms: 
        statements = fn(scheme, var_from, statements)

    return statements


def overlap_free(scheme, var_from: str, statements: list[Statement]) -> list[Statement]:
    bounds = points.boundaries(scheme, var_from)
    
    result = []
    for i in range(len(bounds) - 1):
        x = bounds[i] 
        y = bounds[i + 1]
    
        overlapping = rules.overlapping(statements, Interval(x, y))
        st = rules.intersect(overlapping, Interval(x, y))
        
        if result is not None:
            result.append(st)

    return result


def minimal_height(scheme, var_from, sts: list[Statement]) -> list[Statement]:
    i = 0
    while 0 <= i < len(sts) - 1:
        go_left = False 
        
        if sts[i].domain.end != sts[i + 1].domain.start:
            print("wrong") 
        
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