from collections import defaultdict
from typing import Optional
from z3 import *
import time


from model.points_cache import PointsCache
from model.problem_data import ProblemData
from model.statement import Statement
from model.scheme import Scheme
from model.points import Point, Points
from model.behaviour import Behaviour
import model.variable as vbl
import src.poi as poi


VarKey = tuple[str, str, int]
VarDict = dict[VarKey, ArithRef]


def build_formula(problem_data: ProblemData):
    points_cache = poi.cache_points(problem_data)
    
    vars = build_variables(problem_data, points_cache)
    
    sub_formulas = [
        # phi_max_one, fällt weg
        # phi_gap,     fällt weg
        phi_comp,
        phi_sts, 
        phi_hypothesis,
        phi_comp_nonarb,
    ]

    formula = And(*(
        sub_formula(problem_data, vars, points_cache)
        for sub_formula in sub_formulas
    ))
    
    def solve() -> Optional[Points]:
        s = Solver()
        s.add(formula)
        result = s.check()

        if result != sat:
            return None

        model = s.model()
        return extract_model(problem_data, model, vars, points_cache)
    return solve


def build_variables(problemData: ProblemData, points_cache: PointsCache) -> VarDict: 
    return {
        (a, b, i): Int(f'P_{{{a}, {b}, {i}}}')
        for a in problemData.scheme.variables
        for b in problemData.scheme.order[a]
        for i in range(points_cache.sizes[a])
    }


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


def extract_model(problem_data: ProblemData, model: ModelRef, vars: VarDict, points_cache: PointsCache) -> Points:
    discrete_to_val: dict[str, dict[int, float]] = build_discrete_to_real(problem_data, points_cache)
    
    result: Points = defaultdict(lambda: defaultdict(list))
    for a in problem_data.scheme.variables:
        for b in problem_data.scheme.order[a]:
            for i in range(points_cache.sizes[a]):
                fn_value = model.evaluate(vars[(a, b, i)], model_completion=True)
                assert type(fn_value) == IntNumRef, 'Wrong value found'
                
                result[a][b].append(
                    Point(
                        discrete_to_val[a][i],
                        discrete_to_val[b][fn_value.as_long()]
                    )
                )
        
    return result


def phi_comp_nonarb(problem_data: ProblemData, vars: VarDict, points_cache: PointsCache):
    return And(*(
        Implies(
            And(
                vars[(a, b, i)] == j,
                vars[(a, b, i + 1)] == k
            ),
            Or(
                And(
                    vars[(b, c, l)] <= vars[(b, c, j)]
                    for l in range(j, k + 1)
                ),
                And(
                    vars[(b, c, l)] >= vars[(b, c, j)]
                    for l in range(j, k + 1)
                ) 
            )
        )
        for a in problem_data.scheme.variables
        for c in problem_data.scheme.order[a]
        for b in vbl.pre(problem_data.scheme, c)
        if b in problem_data.scheme.order[a]
        for i in range(points_cache.sizes[a] - 1)
        for j in range(points_cache.sizes[b])
        for k in range(points_cache.sizes[b])
    ))

    
def phi_comp(problem_data: ProblemData, vars: VarDict, points_cache: PointsCache):
    return And(*(
        Implies(
            vars[(a, b, i)] == j,
            vars[(a, c, i)] == vars[(b, c, j)]
        )
        for a in problem_data.scheme.variables
        for c in problem_data.scheme.order[a]
        for b in vbl.pre(problem_data.scheme, c)
        if b in problem_data.scheme.order[a]
        for i in range(points_cache.sizes[a])
        for j in range(points_cache.sizes[b])
    ))  
    
    
def phi_hypothesis(problem_data: ProblemData, vars: VarDict, points_cache: PointsCache):
    hypo = problem_data.hypothesis
    return Or(
        Not(phi_sts_range(problem_data, vars, points_cache, hypo.variableFrom, hypo.variableTo, Statement(hypo.domain, hypo.behaviour, hypo.range))),
        Not(phi_sts_behaviour(problem_data, vars, points_cache, hypo.variableFrom, hypo.variableTo, Statement(hypo.domain, hypo.behaviour, hypo.range)))
    )
    
    
def phi_sts(problem_data: ProblemData, vars: VarDict, points_cache: PointsCache):
    return And(*(
        And(
            phi_sts_range(problem_data, vars, points_cache, a, b, st), 
            phi_sts_behaviour(problem_data, vars, points_cache, a, b, st)
        ) 
        for a, b in problem_data.scheme.statements
        for st in problem_data.scheme.statements[(a, b)]
    ))
    
    
def phi_sts_range(problem_data: ProblemData, vars: VarDict, points_cache: PointsCache, a: str, b: str, st: Statement):
    return And(*(
        And((
            vars[(a, b, i)] <= points_cache.og_points[b][st.range.end],
            points_cache.og_points[b][st.range.start] <= vars[(a, b, i)]
        ))
        for i in range(points_cache.sizes[a]) 
        if points_cache.og_points[a][st.domain.start] <= i <= points_cache.og_points[a][st.domain.end]    
    ))
    

def phi_sts_behaviour(problem_data: ProblemData, vars: VarDict, points_cache: PointsCache, a: str, b: str, st: Statement):
    return And(*(
        phi_behaviour(vars, i, st.behaviour, a, b)
        for i in range(points_cache.sizes[a])
        if points_cache.og_points[a][st.domain.start] <= i 
        if i + 1 <= points_cache.og_points[a][st.domain.end]    
    ))
    

def phi_behaviour(vars: VarDict, i: int, behaviour: Behaviour, a, b):
    if behaviour == Behaviour.MONO:
        return vars[(a, b, i)] <= vars[(a, b, i + 1)]
    if behaviour == Behaviour.ANTI:
        return vars[(a, b, i)] >= vars[(a, b, i + 1)]
    if behaviour == Behaviour.CONST:
        return vars[(a, b, i)] == vars[(a, b, i + 1)]
    return True
