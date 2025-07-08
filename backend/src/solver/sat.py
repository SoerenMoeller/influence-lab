from collections import defaultdict
from typing import Optional
from z3 import *
import time
import os
import re


from model.statement import Statement
from model.scheme import Scheme
from model.behaviour import Behaviour
import src.points as points


VarKey = tuple[str, str, int, int]
VarDict = dict[VarKey, BoolRef]


def build_formula(scheme: Scheme, name: str) -> None:
    if os.path.isfile(f'backend/formulas/{name}.smt2'):
        print(f'Formula "{name}" is already built, skipping building it again..')
        return
    
    print("test")
    
    vars = build_variables(scheme)
    
    sub_formulas = [
        phi_max_one,
        phi_gap,
        phi_comp,
        phi_sts
    ]

    start_build = time.time()
    formula = And(*(
        sub_formula(scheme, vars)
        for sub_formula in sub_formulas
    ))
    end_build = time.time()
    print(f"Formula built in {end_build - start_build:.2f} seconds")
    
    s = Solver()
    s.add(formula)
    with open(f'backend/formulas/{name}.smt2', 'w') as f:
        f.write(s.to_smt2())  


def solve(name: str = 'formula') -> Optional[ModelRef]:
    with open(f'backend/formulas/{name}.smt2', 'r') as f:
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


def build_discrete_to_real(scheme: Scheme) -> dict[str, dict[int, float]]:
    discrete_to_val: dict[str, dict[int, float]] = dict()
    for a in scheme.variables:
        mapping: dict[int, float] = dict()
        bounds = points.boundaries(scheme, a)

        mapping[0] = bounds[0]
        old_point = 0
        old_bound = bounds[0]
        for bound in bounds[1:]:
            distance = points.dist(scheme, a, old_bound, bound)
            new_point = old_point + distance + 1

            mapping[new_point] = bound
            parts = (bound - old_bound) / (distance + 1)
            for i in range(1, distance + 1):
                mapping[old_point + i] = round(parts * i, 2)
            
            old_point = new_point
            old_bound = bound
        
        discrete_to_val[a] = mapping
    return discrete_to_val


def extract_model(scheme: Scheme, model: ModelRef) -> defaultdict[str, defaultdict[str, list[dict[str, float]]]]:
    discrete_to_val: dict[str, dict[int, float]] = build_discrete_to_real(scheme)
    
    positive_vars = extract_positive_vars(model)
    tuples = model_to_points(positive_vars)
    
    result = defaultdict(lambda: defaultdict(list))
    for a, b, x, y in tuples:
        result[a][b].append(
            {
                'x': discrete_to_val[a][x],
                'y': discrete_to_val[b][y]
            }
        )
        
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


def phi_max_one(scheme: Scheme, vars: VarDict):
    return And(*(
        Or(Not(vars[(a, b, i, j)]), Not(vars[(a, b, i, jj)]))
        for a in scheme.variables 
        for b in scheme.order[a]
        for i in range(points.size(scheme, a))
        for j in range(points.size(scheme, b))
        for jj in range(j + 1, points.size(scheme, b))
    ))
    
    
def phi_gap(scheme: Scheme, vars: VarDict):
    return And(*(
        Implies(
            And(vars[(a, b, i, ii)], vars[(a, b, k, kk)]),
            Or(*(
                vars[(a, b, j, jj)]
                for jj in range(points.size(scheme, b))
            ))
        )
        for a in scheme.variables
        for b in scheme.order[a]
        for i in range(points.size(scheme, a))
        for j in range(i + 1, points.size(scheme, a))
        for k in range(j + 1, points.size(scheme, a))
        for ii in range(points.size(scheme, b))
        for kk in range(points.size(scheme, b))
    ))
    
    
def phi_comp(scheme: Scheme, vars: VarDict):
    return And(*(
        Implies(
            And(vars[(a, b, i, j)], vars[(b, c, j, k)]),
            vars[(a, c, i, k)]
        )
        for a in scheme.variables
        for b in scheme.order[a]
        for c in scheme.order[b]
        for i in range(points.size(scheme, a))
        for j in range(points.size(scheme, b))
        for k in range(points.size(scheme, c))
    ))  
    
    
def phi_sts(scheme: Scheme, vars: VarDict):
    return And(*(
        And(
            phi_sts_range(scheme, vars, a, b, st), 
            phi_sts_behaviour(scheme, vars, a, b, st)
        ) 
        for a in scheme.variables
        for b in scheme.order[a]
        for st in scheme.statements[(a, b)]
    ))
    
    
def phi_sts_range(scheme: Scheme, vars: VarDict, a: str, b: str, st: Statement):
    return And(*(
        Or(*(
            vars[(a, b, i, j)]
            for j in range(points.size(scheme, b))
            if points.original_point(scheme, b, st.range.start) <= j <= points.original_point(scheme, b, st.range.end)
        ))
        for i in range(points.size(scheme, a)) 
        if points.original_point(scheme, a, st.domain.start) <= i <= points.original_point(scheme, a, st.domain.end)
    ))
    

def phi_sts_behaviour(scheme: Scheme, vars: VarDict, a: str, b: str, st: Statement):
    return And(*(
        Implies(
            vars[(a, b, i, j)],
            Or(*(
                vars[(a, b, ii, jj)]
                for jj in range(points.size(scheme, b))
                if st.behaviour == Behaviour.MONO or jj >= j
                if st.behaviour == Behaviour.ANTI or jj <= j
                if st.behaviour == Behaviour.CONST or jj == j
            ))
        )
        for i in range(points.size(scheme, a))
        for ii in range(i + 1, points.size(scheme, a))
        for j in range(points.size(scheme, b))
        if points.original_point(scheme, a, st.domain.start) <= i
        if ii <= points.original_point(scheme, a, st.domain.end)
    ))
    

def build_variables(scheme: Scheme) -> VarDict: 
    result = dict()

    for a, b in scheme.statements:
        a_size = points.size(scheme, a) 
        b_size = points.size(scheme, b) 
        
        for i in range(a_size):
            for j in range(b_size):
                result[a, b, i, j] = Bool(f'B_{{{a}, {b}, {i}, {j}}}')
                
    return result