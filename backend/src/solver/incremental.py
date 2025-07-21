import bisect
from collections import defaultdict
from typing import Optional
from z3 import *
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
VarDict = dict[VarKey, ArithRef]
IntermediatePoints = dict[str, dict[tuple[float, float], int]]
PointSet = dict[str, list[int]]


def solve(problem_data: ProblemData) -> Optional[Points]:
    points_cache: PointsCache = poi.cache_points(problem_data)
    
    intermediate = {
        a: {
            (points_cache.boundaries[a][i], points_cache.boundaries[a][i + 1]): 0
            for i in range(len(points_cache.boundaries[a]) - 1)
        }
        for a in problem_data.scheme.variables
    }
    
    vars = build_variables(problem_data, points_cache)
    point_set = current_points(problem_data, points_cache, intermediate)
    
    sub_formulas = [
        # phi_max_one, fällt weg
        # phi_gap,     fällt weg
        phi_comp,
        phi_sts, 
        phi_hypothesis,
        phi_valid,
        phi_comp_nonarb,
    ]

    s = Solver()
    s.set(unsat_core=True)
    
    start_build = time.time()
    for sub_formula in sub_formulas:
        sub_formula(s, problem_data, vars, points_cache, point_set)
    end_build = time.time()
    print(f'Formula built in {end_build - start_build:.2f} seconds')

    # include a second hypothesis
    problem_data.hypothesis = LongStatement('b', Interval(0, 1), Behaviour.CONST, Interval(0, 1), 'c')
    phi_hypothesis(s, problem_data, vars, points_cache, point_set)

    start_solve = time.time()
    result = s.check()
    end_solve = time.time()
    print(f"Solving took {end_solve - start_solve:.2f} seconds")
    print(f'Result: {result}')
    
    if result != 'sat':
        print(s.unsat_core())
        return None
    model = s.model()
    return extract_model(problem_data, model, vars, points_cache, point_set)


def extract_model(problem_data: ProblemData, model: ModelRef, vars: VarDict, 
                  points_cache: PointsCache, point_set: PointSet) -> Points:
    discrete_to_val: dict[str, dict[int, float]] = build_discrete_to_real(problem_data, points_cache)
    
    result: Points = defaultdict(lambda: defaultdict(list))
    for a in problem_data.scheme.variables:
        for b in problem_data.scheme.order[a]:
            for i in point_set[a]:
                fn_value = model.evaluate(vars[(a, b, i)], model_completion=True)
                assert type(fn_value) == IntNumRef, 'Wrong value found'
                
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
        (a, b, i): Int(f'P_{{{a}, {b}, {i}}}')
        for a in problemData.scheme.variables
        for b in problemData.scheme.order[a]
        for i in range(points_cache.sizes[a])
    }
    
    
def phi_comp_nonarb(solver, problem_data: ProblemData, vars: VarDict, 
             points_cache: PointsCache, point_set: PointSet):
    return And(*(
        Implies(
            And(
                vars[(a, b, point_set[a][i])] == j,
                vars[(a, b, point_set[a][i + 1])] == k
            ),
            Or(
                And(
                    vars[(b, c, point_set[b][l])] <= vars[(b, c, j)]
                    for l in range(
                        bisect.bisect_left(point_set[b], j),
                        bisect.bisect_right(point_set[b], k)
                    )
                ),
                And(
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

    

def phi_comp(solver, problem_data: ProblemData, vars: VarDict, 
             points_cache: PointsCache, point_set: PointSet):
    todo = (
        (a, b, c, i, j)
        for a in problem_data.scheme.variables
        for c in problem_data.scheme.order[a]
        for b in vbl.pre(problem_data.scheme, c)
        if b in problem_data.scheme.order[a]
        for i in point_set[a]        
        for j in point_set[b]
    )
    
    for a, b, c, i, j in todo:
        solver.assert_and_track(
            Implies(
                vars[(a, b, i)] == j,
                vars[(a, c, i)] == vars[(b, c, j)]
            ),
            f'comp failed {(a, b, c, i, j)}' 
        )


def phi_sts(solver, problem_data: ProblemData, vars: VarDict, points_cache: PointsCache, point_set: PointSet):
    for a, b in problem_data.scheme.statements:
        for st in problem_data.scheme.statements[(a, b)]:
            phi_sts_range(solver, problem_data, vars, points_cache, point_set, a, b, st)
            phi_sts_behaviour(solver, problem_data, vars, points_cache, point_set, a, b, st)
    
    
def phi_sts_range(solver, problem_data: ProblemData, vars: VarDict, points_cache: PointsCache, 
                  point_set: PointSet, a: str, b: str, st: Statement):
    for i in point_set[a]:
        if not points_cache.og_points[a][st.domain.start] <= i <= points_cache.og_points[a][st.domain.end]:
            continue

        solver.assert_and_track(
            vars[(a, b, i)] <= points_cache.og_points[b][st.range.end],
            f'range failed {(a, b, i, st)} end'
        )
        solver.assert_and_track(
            points_cache.og_points[b][st.range.start] <= vars[(a, b, i)],
            f'range failed {(a, b, i, st)} start'
        ) 
        

def phi_sts_range2(problem_data: ProblemData, vars: VarDict, points_cache: PointsCache, 
                  point_set: PointSet, a: str, b: str, st: Statement):
    return And(*(
        And(
            vars[(a, b, i)] <= points_cache.og_points[b][st.range.end],
            points_cache.og_points[b][st.range.start] <= vars[(a, b, i)],
        )
        for i in point_set[a]
        if points_cache.og_points[a][st.domain.start] <= i <= points_cache.og_points[a][st.domain.end]
    ))
    

def phi_sts_behaviour2(problem_data: ProblemData, vars: VarDict, points_cache: PointsCache, 
                      point_set: PointSet, a: str, b: str, st: Statement):
    return And(*(
        phi_behaviour2(vars, point_set[a][i], point_set[a][i + 1], st.behaviour, a, b)
        for i in range(len(point_set[a]) - 1)
        if points_cache.og_points[a][st.domain.start] <= point_set[a][i]
        if point_set[a][i + 1] <= points_cache.og_points[a][st.domain.end]
    ))
    

def phi_sts_behaviour(solver, problem_data: ProblemData, vars: VarDict, points_cache: PointsCache, 
                      point_set: PointSet, a: str, b: str, st: Statement):
    for i in range(len(point_set[a]) - 1):
        if not points_cache.og_points[a][st.domain.start] <= point_set[a][i]:
            continue
        
        if not point_set[a][i + 1] <= points_cache.og_points[a][st.domain.end]:
            continue
        
        phi_behaviour(solver, vars, point_set[a][i], point_set[a][i + 1], st.behaviour, a, b)
        
    
def phi_behaviour2(vars: VarDict, i: int, next_i: int, behaviour: Behaviour, a, b):
    if behaviour == Behaviour.MONO:
        return vars[(a, b, i)] <= vars[(a, b, next_i)]
    if behaviour == Behaviour.ANTI:
        return vars[(a, b, i)] >= vars[(a, b, next_i)]
    if behaviour == Behaviour.CONST:
        return vars[(a, b, i)] == vars[(a, b, next_i)]
    assert False, 'unreachable'
    

def phi_behaviour(solver, vars: VarDict, i: int, next_i: int, behaviour: Behaviour, a, b):
    if behaviour == Behaviour.MONO:
        solver.assert_and_track(
            vars[(a, b, i)] <= vars[(a, b, next_i)],
            f'behaviour failed {(i, next_i, a, b)} mono'
        )
        return
    if behaviour == Behaviour.ANTI:
        solver.assert_and_track(
            vars[(a, b, i)] >= vars[(a, b, next_i)],
            f'behaviour failed {(i, next_i, a, b)} anti'
        )
        return
    if behaviour == Behaviour.CONST:
        solver.assert_and_track(
            vars[(a, b, i)] == vars[(a, b, next_i)],
            f'behaviour failed {(i, next_i, a, b)} const'
        )
        return
    assert False, 'unreachable'
    

def phi_hypothesis(solver, problem_data: ProblemData, vars: VarDict, points_cache: PointsCache, point_set: PointSet):
    hypo = problem_data.hypothesis
    solver.assert_and_track(
        Or(
            Not(phi_sts_range2(problem_data, vars, points_cache, point_set, hypo.variableFrom, hypo.variableTo, Statement(hypo.domain, hypo.behaviour, hypo.range))),
            Not(phi_sts_behaviour2(problem_data, vars, points_cache, point_set, hypo.variableFrom, hypo.variableTo, Statement(hypo.domain, hypo.behaviour, hypo.range)))
        ),
        f'hypo {problem_data.hypothesis} failed'
    )


def phi_valid(solver, problem_data: ProblemData, vars: VarDict, 
             points_cache: PointsCache, point_set: PointSet):
    for a in problem_data.scheme.variables:
        for b in problem_data.scheme.order[a]:
            for i in point_set[a]:
                solver.assert_and_track(
                    Or(*(
                        vars[(a, b, i)] == j
                        for j in point_set[b] 
                    )),
                    f'valid failed {(a, b, i)}'
                )
