from collections import defaultdict
from typing import Optional
from z3 import *


from model.points_cache import PointsCache
from model.problem_data import ProblemData
from model.statement import Statement
from model.scheme import Scheme
from model.points import Point, Points
from model.behaviour import Behaviour
import model.variable as vbl
import src.poi as poi


VarKey = tuple[str, str, int, int]
VarDict = dict[VarKey, BoolRef]


def build_formula(problem_data: ProblemData):
    points_cache = poi.cache_points(problem_data)
    vars = build_variables(problem_data, points_cache)
    
    sub_formulas = [
        phi_max_one,
        # phi_gap, probably unnecessary?
        phi_comp,
        phi_sts, 
        phi_hypothesis,
        phi_comp_nonarb,
    ]

    formula = And(*(
        sub_formula(problem_data, points_cache, vars)
        for sub_formula in sub_formulas
    ))
    
    def solve() -> Optional[Points]:
        s = Solver()
        s.add(formula)

        result = s.check()
        model = s.model()

        if not result:
            return None
        return extract_model(problem_data, points_cache, model, vars)

    return solve


def build_discrete_to_real(problem_data: ProblemData, points_cache: PointsCache) -> dict[str, dict[int, float]]:
    discrete_to_val: dict[str, dict[int, float]] = dict()
    for a in problem_data.scheme.variables:
        mapping: dict[int, float] = dict()
        bounds = points_cache.boundaries[a]

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


def extract_model(problem_data: ProblemData, points_cache: PointsCache, model: ModelRef, vars) -> Points:
    discrete_to_val: dict[str, dict[int, float]] = build_discrete_to_real(problem_data, points_cache)
    tuples = extract_positive_vars(problem_data, points_cache, model, vars)
    
    result: Points = defaultdict(lambda: defaultdict(list))
    for a, b, x, y in tuples:
        result[a][b].append(Point(discrete_to_val[a][x], discrete_to_val[b][y]))
        
    return result

    
def extract_positive_vars(problem_data: ProblemData, points_cache: PointsCache, model: ModelRef, vars) -> list[tuple]:
    result = []
    for a in problem_data.scheme.variables:
        for b in problem_data.scheme.order[a]:
            for i in range(points_cache.sizes[a]):
                for j in range(points_cache.sizes[b]):
                    var_value = model.evaluate(vars[(a, b, i, j)], model_completion=True)
                    assert type(var_value) == BoolRef, 'Wrong result'
                        
                    if var_value.py_value():
                        result.append((a, b, i, j))
    return result
    
    
def phi_max_one(problem_data: ProblemData, points_cache: PointsCache, vars: VarDict):
    return And(*(
        Or(Not(vars[(a, b, i, j)]), Not(vars[(a, b, i, jj)]))
        for a in problem_data.scheme.variables 
        for b in problem_data.scheme.order[a]
        for i in range(points_cache.sizes[a])
        for j in range(points_cache.sizes[b])
        for jj in range(j + 1, points_cache.sizes[b])
    ))
    

def phi_comp_nonarb(problem_data: ProblemData, points_cache: PointsCache, vars: VarDict):
    return And(*(
        Implies(
            And(
                vars[(a, b, i, j)],
                vars[(a, b, i + 1, k)],
                vars[(b, c, j, l)]
            ),
            Or(
                And(*(
                    Or(*(
                        vars[(b, c, jj, ll)]
                        for ll in range(points_cache.sizes[c])
                        if ll >= l
                    ))
                    for jj in range(j, k + 1)
                )),
                And(*(
                    Or(*(
                        vars[(b, c, jj, ll)]
                        for ll in range(points_cache.sizes[c])
                        if ll <= l
                    ))
                    for jj in range(j, k + 1)
                )),
            )
        )
        for a in problem_data.scheme.variables
        for c in problem_data.scheme.order[a]
        for b in vbl.pre(problem_data.scheme, c)
        if b in problem_data.scheme.order[a]
        for i in range(points_cache.sizes[a] - 1)
        for j in range(points_cache.sizes[b])
        for k in range(points_cache.sizes[b])
        for l in range(points_cache.sizes[c])
    ))  
    
    
def phi_comp(problem_data: ProblemData, points_cache: PointsCache, vars: VarDict):
    return And(*(
        Implies(
            And(vars[(a, b, i, j)], vars[(b, c, j, k)]),
            vars[(a, c, i, k)]
        )
        for a in problem_data.scheme.variables
        for c in problem_data.scheme.order[a]
        for b in vbl.pre(problem_data.scheme, c)
        if b in problem_data.scheme.order[a]
        for i in range(points_cache.sizes[a])
        for j in range(points_cache.sizes[b])
        for k in range(points_cache.sizes[c])
    ))  
    
    
def phi_hypothesis(problem_data: ProblemData, points_cache: PointsCache, vars: VarDict):
    hypo = problem_data.hypothesis
    return Or(
        Not(phi_sts_range(problem_data, points_cache, vars, hypo.variableFrom, hypo.variableTo, Statement(hypo.domain, hypo.behaviour, hypo.range))),
        Not(phi_sts_behaviour(problem_data, points_cache, vars, hypo.variableFrom, hypo.variableTo, Statement(hypo.domain, hypo.behaviour, hypo.range)))
    )
    
    
def phi_sts(problem_data: ProblemData, points_cache: PointsCache, vars: VarDict):
    return And(*(
        And(
            phi_sts_range(problem_data, points_cache, vars, a, b, st), 
            phi_sts_behaviour(problem_data, points_cache, vars, a, b, st)
        ) 
        for a, b in problem_data.scheme.statements
        for st in problem_data.scheme.statements[(a, b)]
    ))
    
    
def phi_sts_range(problem_data: ProblemData, points_cache: PointsCache, vars: VarDict, a: str, b: str, st: Statement):
    return And(*(
        Or(*(
            vars[(a, b, i, j)]
            for j in range(points_cache.sizes[b])
            if points_cache.og_points[b][st.range.start] <= j <= points_cache.og_points[b][st.range.end]
        ))
        for i in range(points_cache.sizes[a]) 
        if points_cache.og_points[a][st.domain.start] <= i <= points_cache.og_points[a][st.domain.end]
    ))
    

def phi_sts_behaviour(problem_data: ProblemData, points_cache: PointsCache, vars: VarDict, a: str, b: str, st: Statement):
    return And(*(
        Implies(
            vars[(a, b, i, j)],
            Or(*(
                vars[(a, b, ii, jj)]
                for jj in range(points_cache.sizes[b])
                if st.behaviour == Behaviour.MONO or jj >= j
                if st.behaviour == Behaviour.ANTI or jj <= j
                if st.behaviour == Behaviour.CONST or jj == j
            ))
        )
        for i in range(points_cache.sizes[a])
        for ii in range(i + 1, points_cache.sizes[a])
        for j in range(points_cache.sizes[b])
        if points_cache.og_points[a][st.domain.start] <= i
        if ii <=  points_cache.og_points[a][st.domain.end]    
    ))
    

def build_variables(problemData: ProblemData, points_cache: PointsCache) -> VarDict: 
    result = dict()

    for a, b in problemData.scheme.statements:
        a_size = points_cache.sizes[a]
        b_size = points_cache.sizes[b]
        
        for i in range(a_size):
            for j in range(b_size):
                result[(a, b, i, j)] = Bool(f'B_{{{a}, {b}, {i}, {j}}}')
                
    return result
