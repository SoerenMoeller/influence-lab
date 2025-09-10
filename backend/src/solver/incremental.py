import bisect
from collections import defaultdict
from typing import Optional
import z3
import time


from model.interval import Interval
from model.points_cache import PointsCache
from model.problem_data import ProblemData
from model.statement import LongStatement, Statement
from model.points import Point, Points
from model.behaviour import Behaviour
import model.variable as vbl
import src.poi as poi


VarKey = tuple[str, str, int]
VarDict = dict[VarKey, z3.ArithRef]
IntermediatePoints = dict[str, dict[tuple[float, float], int]]
PointSet = dict[str, list[int]]


def build_formula(problem_data: ProblemData):
    points_cache: PointsCache = poi.cache_points(problem_data)
    
    intermediate = {
        a: {
            (points_cache.boundaries[a][i], points_cache.boundaries[a][i + 1]): 0
            for i in range(len(points_cache.boundaries[a]) - 1)
        }
        for a in problem_data.scheme.variables
    }
    
    vars = build_variables(problem_data, points_cache)

    def solve() -> Optional[Points]:
        while True:
            point_set = current_points(problem_data, points_cache, intermediate)

            result, solver = attempt_solving(problem_data, vars, points_cache, point_set)
            if result == z3.sat:
                model = solver.model()
                return extract_model(problem_data, model, vars, points_cache, point_set)
            
            problems = [parse_pattern(str(reason)) for reason in solver.unsat_core()]
            problem_vars = {b for _, b, _ in problems} 

            for var in problem_vars:
                for pair in intermediate[var]:
                    if intermediate[var][pair] == points_cache.poi_sizes[var][pair]:
                        return None
                    intermediate[var][pair] += 1
    return solve
    
    
def parse_pattern(content: str):
    assert content.startswith('F('), 'Prefix missing'
    content = content[2:]
    
    contents = content.split(',')
    assert len(contents) == 2, 'There should only be one comma'
   
    var1 = contents[0] 
    content = contents[1]
    
    contents = content.split(')')
    assert len(contents) == 3, 'There should only be two closing brackets'

    var2 = contents[0]
    
    assert contents[1].startswith('('), 'Should start with opening bracket'
    content = contents[1][1:]
    
    assert content.isdigit(), 'Should be a number'
    value = int(content)
    
    return var1, var2, value


def attempt_solving(problem_data, vars, points_cache, point_set):
    solver = z3.Solver()
    solver.set('core.minimize', True)  
    solver.set(unsat_core=True)
    
    sub_formulas = [
        phi_comp,
        phi_sts, 
        phi_hypothesis,
        phi_comp_nonarb,
    ]

    solver.add(
        z3.And(*(
            sub_formula(problem_data, vars, points_cache, point_set)
            for sub_formula in sub_formulas
        )
    ))
    phi_valid_points(solver, problem_data, vars, points_cache, point_set)
    

    result = solver.check()
    
    return result, solver

def extract_model(problem_data: ProblemData, model: z3.ModelRef, vars: VarDict, 
                  points_cache: PointsCache, point_set: PointSet) -> Points:
    discrete_to_val: dict[str, dict[int, float]] = build_discrete_to_real(problem_data, points_cache)
    
    result: Points = defaultdict(lambda: defaultdict(list))
    for a in problem_data.scheme.variables:
        for b in problem_data.scheme.order[a]:
            for i in point_set[a]:
                fn_value = model.evaluate(vars[(a, b, i)], model_completion=True)
                assert type(fn_value) == z3.IntNumRef, 'Wrong value found'
                
                result[a][b].append(
                    Point(
                        discrete_to_val[a][i],
                        discrete_to_val[b][fn_value.as_long()]
                    )
                )
     
    return result


def build_discrete_to_real(problem_data: ProblemData, points_cache: PointsCache) -> dict[str, dict[int, float]]:
    discrete_to_val: dict[str, dict[int, float]] = dict()
    for a in problem_data.scheme.variables:
        mapping: dict[int, float] = dict()
        bounds = poi.boundaries(problem_data, a)

        mapping[0] = bounds[0]
        old_point = 0
        old_bound = bounds[0]
        for bound in bounds[1:]:
            distance = poi.dist(problem_data, points_cache, a, old_bound, bound)
            new_point = old_point + distance + 1
            mapping[new_point] = bound
            parts = (bound - old_bound) / (distance + 1)
            for i in range(1, distance + 1):
                mapping[old_point + i] = old_bound + round(parts * i, 2)
            
            old_point = new_point
            old_bound = bound
        
        discrete_to_val[a] = mapping
    return discrete_to_val


def current_points(problem_data: ProblemData, points_cache: PointsCache, 
                   intermediate: IntermediatePoints) -> PointSet:
    result: PointSet = dict()
    for a in problem_data.scheme.variables:
        points = [0]
        last_point = 0
        for i in range(1, len(points_cache.boundaries[a])):
            b1 = points_cache.boundaries[a][i - 1]
            b2 = points_cache.boundaries[a][i]

            end_point = last_point + 1 + intermediate[a][(b1, b2)]
            points += list(range(last_point + 1, end_point))

            bound_point = points_cache.og_points[a][b2]
            points.append(bound_point)
            
            last_point = bound_point 
            
        result[a] = points
        
    return result


def build_variables(problemData: ProblemData, points_cache: PointsCache) -> VarDict: 
    return {
        (a, b, i): z3.Int(f'P_{{{a}, {b}, {i}}}')
        for a in problemData.scheme.variables
        for b in problemData.scheme.order[a]
        for i in range(points_cache.sizes[a])
    }
    
    
def phi_comp_nonarb(problem_data: ProblemData, vars: VarDict, 
             points_cache: PointsCache, point_set: PointSet):
    return z3.And(*(
        z3.Implies(
            z3.And(
                vars[(a, b, point_set[a][i])] == j,
                vars[(a, b, point_set[a][i + 1])] == k
            ),
            z3.Or(
                z3.And(
                    vars[(b, c, point_set[b][l])] <= vars[(b, c, j)]
                    for l in range(
                        bisect.bisect_left(point_set[b], j),
                        bisect.bisect_right(point_set[b], k)
                    )
                ),
                z3.And(
                    vars[(b, c, l)] >= vars[(b, c, j)]
                    for l in range(
                        bisect.bisect_left(point_set[b], j),
                        bisect.bisect_right(point_set[b], k)
                    )
                ) 
            )
        )
        for a in problem_data.scheme.variables
        for c in problem_data.scheme.order[a]
        for b in vbl.pre(problem_data.scheme, c)
        if b in problem_data.scheme.order[a]
        for i in range(len(point_set[a]) - 1)
        for j in point_set[b]
        for k in point_set[b]
    ))

    

def phi_comp(problem_data: ProblemData, vars: VarDict, 
             points_cache: PointsCache, point_set: PointSet):
    return z3.And(*(
        z3.Implies(
            vars[(a, b, i)] == j,
            vars[(a, c, i)] == vars[(b, c, j)]
        )
        for a in problem_data.scheme.variables
        for c in problem_data.scheme.order[a]
        for b in vbl.pre(problem_data.scheme, c)
        if b in problem_data.scheme.order[a]
        for i in point_set[a]        
        for j in point_set[b]
    ))


def phi_sts(problem_data: ProblemData, vars: VarDict, points_cache: PointsCache, point_set: PointSet):
    return z3.And(*(
        z3.And(
            phi_sts_range(problem_data, vars, points_cache, point_set, a, b, st),
            phi_sts_behaviour(problem_data, vars, points_cache, point_set, a, b, st)
        )
        for a, b in problem_data.scheme.statements
        for st in problem_data.scheme.statements[(a, b)]
    ))
    
    
def phi_sts_range(problem_data: ProblemData, vars: VarDict, points_cache: PointsCache, 
                  point_set: PointSet, a: str, b: str, st: Statement):
    return z3.And(*(
        z3.And(
            vars[(a, b, i)] <= points_cache.og_points[b][st.range.end],
            points_cache.og_points[b][st.range.start] <= vars[(a, b, i)]
        )
        
        for i in point_set[a]
        if points_cache.og_points[a][st.domain.start] <= i <= points_cache.og_points[a][st.domain.end]
    ))
        

def phi_sts_behaviour(problem_data: ProblemData, vars: VarDict, points_cache: PointsCache, 
                      point_set: PointSet, a: str, b: str, st: Statement):
    return z3.And(*(
        phi_behaviour(vars, point_set[a][i], point_set[a][i + 1], st.behaviour, a, b)
        for i in range(len(point_set[a]) - 1)
        if points_cache.og_points[a][st.domain.start] <= point_set[a][i]
        if point_set[a][i + 1] <= points_cache.og_points[a][st.domain.end]
    ))
    

def phi_behaviour(vars: VarDict, i: int, next_i: int, behaviour: Behaviour, a, b):
    if behaviour == Behaviour.MONO:
        return vars[(a, b, i)] <= vars[(a, b, next_i)]
    if behaviour == Behaviour.ANTI:
        return vars[(a, b, i)] >= vars[(a, b, next_i)]
    if behaviour == Behaviour.CONST:
        return vars[(a, b, i)] == vars[(a, b, next_i)]
    return True 

def phi_hypothesis(problem_data: ProblemData, vars: VarDict, points_cache: PointsCache, point_set: PointSet):
    hypo = problem_data.hypothesis
    shortHypo = Statement(hypo.domain, hypo.behaviour, hypo.range)
    a, b = hypo.variableFrom, hypo.variableTo
    return z3.Or(
        z3.Not(phi_sts_range(problem_data, vars, points_cache, point_set, a, b, shortHypo)),
        z3.Not(phi_sts_behaviour(problem_data, vars, points_cache, point_set, a, b, shortHypo))
    )


def phi_valid_points(solver, problem_data: ProblemData, vars: VarDict, 
             points_cache: PointsCache, point_set: PointSet):
    for a in problem_data.scheme.variables:
        for b in problem_data.scheme.order[a]:
            for i in point_set[a]:
                solver.assert_and_track(
                    z3.Or(*(
                        vars[(a, b, i)] == j
                        for j in point_set[b] 
                    )),
                    f'F({a},{b})({i})'
                )
