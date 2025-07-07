import bisect
from model.scheme import Scheme
import model.variable as vbl

def boundaries(scheme: Scheme, variable: str) -> list[float]:
    statementsFrom = [st for var in vbl.post(scheme, variable) for st in scheme.statements[variable, var]]
    statementsTo = [st for var in vbl.pre(scheme, variable) for st in scheme.statements[var, variable]]

    bounds = set()
    for statement in statementsFrom:
        bounds.add(statement.domain.start)
        bounds.add(statement.domain.end)
    for statement in statementsTo:
        bounds.add(statement.range.start)
        bounds.add(statement.range.end)
        
    return sorted(bounds)

def dist_tp(scheme: Scheme, variable: str, x: float, y: float) -> int:
    return sum(
        dist_tp2(scheme, variable, var2, x, y) for var2 in vbl.post(scheme, variable)
    )

def dist_tp2(scheme: Scheme, var1: str, var2: str, x: float, y: float) -> int: 
    if vbl.is_maximal(var1, scheme):
        return 0
    
    scheme
    
    print(f'x={x}, y={y}, var1={var1}, var2={var2}')
    bounds = boundaries(scheme, var2)
    print(f'all bounds: {bounds}')
    left_end = bisect.bisect(bounds, x)
    right_end = bisect.bisect(bounds, y)
    bounds = bounds[left_end:right_end + 1]
    print(f'bounds: {bounds}')
    # for i, j in zip(bounds, bounds[:-1]):
    #     bounds.bisect

    

    return 2
    # for i in range()
    # return result
