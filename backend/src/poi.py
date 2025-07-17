import bisect
from collections import defaultdict
from model.points_cache import PointsCache
from model.interval import Interval
from model.scheme import Scheme
from model.problem_data import ProblemData
import model.variable as vbl
import model.interval as ivl


def cache_points(problem_data: ProblemData) -> PointsCache:
    boundaries_ = {
        a: boundaries(problem_data, a) 
        for a in problem_data.scheme.variables
    }
    
    points_cache = PointsCache(
        boundaries_, defaultdict(dict), defaultdict(dict), dict(), dict()
    )
    
    for a in problem_data.scheme.variables:
        for i in range(len(boundaries_[a]) - 1):
            dist_tp(problem_data, points_cache, a, boundaries_[a][i], boundaries_[a][i + 1]) 
            
    for a in problem_data.scheme.variables:
        for i in range(len(boundaries_[a]) - 1):
            dist_poi(problem_data.scheme, points_cache, a, boundaries_[a][i], boundaries_[a][i + 1]) 
            
    points_cache.sizes = {
        a: size(problem_data, points_cache, a)
        for a in problem_data.scheme.variables
    }
    
    points_cache.og_points = {
        a: {
            bound: original_point(problem_data, points_cache, a, bound) 
            for bound in boundaries_[a]
        }
        for a in problem_data.scheme.variables
    }
            
    return points_cache


def boundaries(problem_data: ProblemData, variable: str) -> list[float]:
    scheme = problem_data.scheme
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
        
    if problem_data.hypothesis.variableFrom == variable:
        bounds.add(problem_data.hypothesis.domain.start) 
        bounds.add(problem_data.hypothesis.domain.end) 
        
    if problem_data.hypothesis.variableTo == variable:
        bounds.add(problem_data.hypothesis.range.start) 
        bounds.add(problem_data.hypothesis.range.end) 
        
    return sorted(bounds)


def dist_tp(problem_data: ProblemData, points_cache: PointsCache, 
            variable: str, x: float, y: float) -> int:
    if (x, y) in points_cache.tp_sizes[variable]: 
        return points_cache.tp_sizes[variable][(x, y)]

    result = sum(
        dist_tp2(problem_data, points_cache, variable, var2, x, y) 
        for var2 in vbl.post(problem_data.scheme, variable)
    )
    points_cache.tp_sizes[variable][(x, y)] = result
    
    return result


def dist_tp2(problem_data: ProblemData, points_cache: PointsCache,
             var1: str, var2: str, x: float, y: float) -> int: 
    if vbl.is_maximal(var1, problem_data.scheme):
        return 0
    
    sts = [
        st 
        for st in problem_data.scheme.statements[(var1, var2)] 
        if st.domain == Interval(x, y)
    ]
    assert sts, 'No statement found' 
    st = sts[0]
    
    bounds = [
        bound 
        for bound in points_cache.boundaries[var2] 
        if st.range.start <= bound <= st.range.end
    ]
    
    result = 2
    for i in range(len(bounds) - 1):
        result += 2 + dist_tp(problem_data, points_cache, var2, bounds[i], bounds[i + 1])
        
    return result


def dom_inverse(scheme: Scheme, var1: str, var2: str, x: float, y: float) -> list[Interval]:
    sts = scheme.statements[(var1, var2)]
    return [st.domain for st in sts if ivl.subinterval(Interval(x, y), st.range)]


def dist_poi(scheme: Scheme, points_cache: PointsCache, var: str, x: float, y: float) -> int:
    if (x, y) in points_cache.poi_sizes[var]:
        return points_cache.poi_sizes[var][(x, y)]

    result = 0
    for var2 in vbl.pre(scheme, var):
        result += dist_poi2(scheme, points_cache, var2, var, x, y)
    points_cache.poi_sizes[var][(x, y)] = result     
    
    return result


def dist_poi2(scheme: Scheme, points_cache: PointsCache, 
              var1: str, var2: str, x: float, y: float) -> int:
    doms = [dom.to_tuple() for dom in dom_inverse(scheme, var1, var2, x, y)]

    result = 0
    for x1, y1 in doms:
        result += 2 + dist_poi(scheme, points_cache, var1, x1 ,y1)
    return result


def dist(problem_data: ProblemData, points_cache: PointsCache, 
         var: str, x: float, y: float) -> int:
    return dist_tp(problem_data, points_cache, var, x, y) \
        + dist_poi(problem_data.scheme, points_cache, var, x, y)


def original_point(problem_data: ProblemData, points_cache: PointsCache, 
                   var: str, x: float) -> int:
    bounds = boundaries(problem_data, var)
    result = 0
    
    idx = bisect.bisect(bounds, x)
    bounds = bounds[:idx]

    for i in range(len(bounds) - 1):
        result += 1 + dist(problem_data, points_cache, var, bounds[i], bounds[i + 1])
        
    return result    


def size(problem_data: ProblemData, points_cache: PointsCache, var: str) -> int:
    bounds = boundaries(problem_data, var)
    
    result = 1
    for i in range(len(bounds) - 1):
        result += 1 + dist(problem_data, points_cache, var, bounds[i], bounds[i + 1])
        
    return result