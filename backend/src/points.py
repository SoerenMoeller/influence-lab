import bisect
from model.interval import Interval
from model.scheme import Scheme
import model.variable as vbl
import model.interval as ivl


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
    
    bounds = boundaries(scheme, var2)
    st = [st for st in scheme.statements[(var1, var2)] if st.domain == Interval(x, y)][0]
    left_end = bisect.bisect(bounds, st.range.start)
    right_end = bisect.bisect(bounds, st.range.end)
    bounds = bounds[left_end:right_end + 1]
    
    result = 2
    for i in range(len(bounds) - 1):
        result += dist_tp(scheme, var2, bounds[i], bounds[i + 1])
        
    return result


def dom_inverse(scheme: Scheme, var1: str, var2: str, x: float, y: float) -> list[Interval]:
    sts = scheme.statements[(var1, var2)]
    return [st.domain for st in sts if ivl.subinterval(Interval(x, y), st.range)]


def dist_poi(scheme: Scheme, var: str, x: float, y: float) -> int:
    result = 0
    for var2 in vbl.pre(scheme, var):
        result += dist_poi2(scheme, var2, var, x, y)
    return result


def dist(scheme: Scheme, var: str, x: float, y: float) -> int:
    return dist_tp(scheme, var, x, y) + dist_poi(scheme, var, x, y)


def dist_poi2(scheme: Scheme, var1: str, var2: str, x: float, y: float) -> int:
    doms = [dom.to_tuple() for dom in dom_inverse(scheme, var1, var2, x, y)]

    result = 0
    for x1, y1 in doms:
        result += dist_poi(scheme, var1, x1 ,y1)
    return result


def get_original_point(scheme: Scheme, var: str, x: float) -> int:
    bounds = boundaries(scheme, var)
    result = 0

    for i in range(len(bounds) - 1):
        if x > bounds[i + 1]:
            break
        
        result += 1 + dist(scheme, var, bounds[i], bounds[i + 1])
        
    return result    
