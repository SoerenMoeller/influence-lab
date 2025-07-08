import bisect
from model.interval import Interval
from model.scheme import Scheme
import model.variable as vbl
import model.interval as ivl


def boundaries(scheme: Scheme, variable: str) -> list[float]:
    statementsFrom = [st for var in scheme.order[variable] for st in scheme.statements[variable, var]]
    pres = [var for var in scheme.variables if variable in scheme.order[var]]
    statementsTo = [st for var in pres for st in scheme.statements[var, variable]]

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
    bounds = [bound for bound in bounds if st.range.start <= bound <= st.range.end]
    
    result = 2
    for i in range(len(bounds) - 1):
        result += 2 + dist_tp(scheme, var2, bounds[i], bounds[i + 1])
        
    return result


def dom_inverse(scheme: Scheme, var1: str, var2: str, x: float, y: float) -> list[Interval]:
    sts = scheme.statements[(var1, var2)]
    return [st.domain for st in sts if ivl.subinterval(Interval(x, y), st.range)]


def dist_poi(scheme: Scheme, var: str, x: float, y: float) -> int:
    result = 0
    for var2 in vbl.pre(scheme, var):
        result += dist_poi2(scheme, var2, var, x, y)
    return result


def dist_poi2(scheme: Scheme, var1: str, var2: str, x: float, y: float) -> int:
    doms = [dom.to_tuple() for dom in dom_inverse(scheme, var1, var2, x, y)]

    result = 0
    for x1, y1 in doms:
        result += 2 + dist_poi(scheme, var1, x1 ,y1)
    return result


def dist(scheme: Scheme, var: str, x: float, y: float) -> int:
    return dist_tp(scheme, var, x, y) + dist_poi(scheme, var, x, y)


def original_point(scheme: Scheme, var: str, x: float) -> int:
    bounds = boundaries(scheme, var)
    result = 0
    
    idx = bisect.bisect(bounds, x)
    bounds = bounds[:idx]

    for i in range(len(bounds) - 1):
        result += 1 + dist(scheme, var, bounds[i], bounds[i + 1])
        
    return result    


def size(scheme: Scheme, var: str) -> int:
    bounds = boundaries(scheme, var)
    
    result = 1
    for i in range(len(bounds) - 1):
        result += 1 + dist(scheme, var, bounds[i], bounds[i + 1])
        
    return result