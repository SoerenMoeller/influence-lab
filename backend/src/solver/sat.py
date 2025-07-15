from collections import defaultdict
from typing import Optional
from z3 import *
import time
import os
import re


from model.problem_data import ProblemData
from model.statement import Statement
from model.scheme import Scheme
from model.points import Point, Points
from model.behaviour import Behaviour
import src.poi as poi


VarKey = tuple[str, str, int, int]
VarDict = dict[VarKey, BoolRef]


def build_formula(problem_data: ProblemData, name: str) -> None:
    if os.path.isfile(f'formulas/{name}.smt2'):
        print(f'Formula "{name}" is already built, skipping building it again..')
        return
    
    vars = build_variables(problem_data)
    
    sub_formulas = [
        phi_max_one,
        phi_gap,
        phi_comp,
        phi_sts, 
        phi_hypothesis
    ]

    start_build = time.time()
    formula = And(*(
        sub_formula(problem_data, vars)
        for sub_formula in sub_formulas
    ))
    end_build = time.time()
    print(f"Formula built in {end_build - start_build:.2f} seconds")
    
    s = Solver()
    s.add(formula)
    with open(f'formulas/{name}.smt2', 'w') as f:
        f.write(s.to_smt2())  


def solve(name: str = 'formula') -> Optional[ModelRef]:
    with open(f'formulas/{name}.smt2', 'r') as f:
        smt2 = f.read() 
    
    s = Solver()
    s.from_string(smt2)

    start_solve = time.time()
    result = s.check()
    model = s.model()
    end_solve = time.time()
    print(f"Solving took {end_solve - start_solve:.2f} seconds")
    print(f'Result: {result}')

    if not result:
        return None
    return model


def build_discrete_to_real(problem_data: ProblemData) -> dict[str, dict[int, float]]:
    discrete_to_val: dict[str, dict[int, float]] = dict()
    for a in problem_data.scheme.variables:
        mapping: dict[int, float] = dict()
        bounds = poi.boundaries(problem_data, a)

        mapping[0] = bounds[0]
        old_point = 0
        old_bound = bounds[0]
        for bound in bounds[1:]:
            distance = poi.dist(problem_data, a, old_bound, bound)
            new_point = old_point + distance + 1

            mapping[new_point] = bound
            parts = (bound - old_bound) / (distance + 1)
            for i in range(1, distance + 1):
                mapping[old_point + i] = old_bound + round(parts * i, 2)
            
            old_point = new_point
            old_bound = bound
        
        discrete_to_val[a] = mapping
    return discrete_to_val


def extract_model(problem_data: ProblemData, model: ModelRef) -> Points:
    discrete_to_val: dict[str, dict[int, float]] = build_discrete_to_real(problem_data)
    
    positive_vars = extract_positive_vars(model)
    tuples = model_to_points(positive_vars)
    
    result: Points = defaultdict(lambda: defaultdict(list))
    for a, b, x, y in tuples:
        result[a][b].append(Point(discrete_to_val[a][x], discrete_to_val[b][y]))
        
    return result

    
def extract_positive_vars(model) -> list[str]:
    positive_vars = []
    for d in model.decls():
        var_name = d.name()
        var_value = model[d]
        if is_true(var_value):
            positive_vars.append(var_name)
    return positive_vars
    
    
def model_to_points(positives: list[str]) -> list[VarKey]:
    pattern = r"B_\{\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^}]+)\s*\}"

    result = []
    for var in positives:
        match = re.match(pattern, var)
        assert match, f'Could not extract value for "{var}"'

        group1, group2, group3, group4 = match.groups()
        result.append((group1, group2, int(group3), int(group4)))
    return result


def phi_max_one(problem_data: ProblemData, vars: VarDict):
    return And(*(
        Or(Not(vars[(a, b, i, j)]), Not(vars[(a, b, i, jj)]))
        for a in problem_data.scheme.variables 
        for b in problem_data.scheme.order[a]
        for i in range(poi.size(problem_data, a))
        for j in range(poi.size(problem_data, b))
        for jj in range(j + 1, poi.size(problem_data, b))
    ))
    
    
def phi_gap(problem_data: ProblemData, vars: VarDict):
    return And(*(
        Implies(
            And(vars[(a, b, i, ii)], vars[(a, b, k, kk)]),
            Or(*(
                vars[(a, b, j, jj)]
                for jj in range(poi.size(problem_data, b))
            ))
        )
        for a in problem_data.scheme.variables
        for b in problem_data.scheme.order[a]
        for i in range(poi.size(problem_data, a))
        for j in range(i + 1, poi.size(problem_data, a))
        for k in range(j + 1, poi.size(problem_data, a))
        for ii in range(poi.size(problem_data, b))
        for kk in range(poi.size(problem_data, b))
    ))
    
    
def phi_comp(problem_data: ProblemData, vars: VarDict):
    return And(*(
        Implies(
            And(vars[(a, b, i, j)], vars[(b, c, j, k)]),
            vars[(a, c, i, k)]
        )
        for a in problem_data.scheme.variables
        for b in problem_data.scheme.order[a]
        for c in problem_data.scheme.order[b]
        for i in range(poi.size(problem_data, a))
        for j in range(poi.size(problem_data, b))
        for k in range(poi.size(problem_data, c))
    ))  
    
    
def phi_hypothesis(problem_data: ProblemData, vars: VarDict):
    hypo = problem_data.hypothesis
    return Or(
        Not(phi_sts_range(problem_data, vars, hypo.variableFrom, hypo.variableTo, Statement(hypo.domain, hypo.behaviour, hypo.range))),
        Not(phi_sts_behaviour(problem_data, vars, hypo.variableFrom, hypo.variableTo, Statement(hypo.domain, hypo.behaviour, hypo.range)))
    )
    
    
def phi_sts(problem_data: ProblemData, vars: VarDict):
    return And(*(
        And(
            phi_sts_range(problem_data, vars, a, b, st), 
            phi_sts_behaviour(problem_data, vars, a, b, st)
        ) 
        for a in problem_data.scheme.variables
        for b in problem_data.scheme.order[a]
        for st in problem_data.scheme.statements[(a, b)]
    ))
    
    
def phi_sts_range(problem_data: ProblemData, vars: VarDict, a: str, b: str, st: Statement):
    return And(*(
        Or(*(
            vars[(a, b, i, j)]
            for j in range(poi.size(problem_data, b))
            if poi.original_point(problem_data, b, st.range.start) <= j <= poi.original_point(problem_data, b, st.range.end)
        ))
        for i in range(poi.size(problem_data, a)) 
        if poi.original_point(problem_data, a, st.domain.start) <= i <= poi.original_point(problem_data, a, st.domain.end)
    ))
    

def phi_sts_behaviour(problem_data: ProblemData, vars: VarDict, a: str, b: str, st: Statement):
    return And(*(
        Implies(
            vars[(a, b, i, j)],
            Or(*(
                vars[(a, b, ii, jj)]
                for jj in range(poi.size(problem_data, b))
                if st.behaviour == Behaviour.MONO or jj >= j
                if st.behaviour == Behaviour.ANTI or jj <= j
                if st.behaviour == Behaviour.CONST or jj == j
            ))
        )
        for i in range(poi.size(problem_data, a))
        for ii in range(i + 1, poi.size(problem_data, a))
        for j in range(poi.size(problem_data, b))
        if poi.original_point(problem_data, a, st.domain.start) <= i
        if ii <= poi.original_point(problem_data, a, st.domain.end)
    ))
    

def build_variables(problemData: ProblemData) -> VarDict: 
    result = dict()

    for a, b in problemData.scheme.statements:
        a_size = poi.size(problemData, a) 
        b_size = poi.size(problemData, b) 
        
        for i in range(a_size):
            for j in range(b_size):
                result[a, b, i, j] = Bool(f'B_{{{a}, {b}, {i}, {j}}}')
                
    return result