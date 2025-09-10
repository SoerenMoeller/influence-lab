from collections import defaultdict
from typing import Optional
from z3 import *
from model.points import Point, Points
from model.scheme import Scheme
from model.behaviour import Behaviour
from model.problem_data import ProblemData
import model.variable as vbl
import src.poi as poi


def build_formula(problem_data: ProblemData):
    experiment = create_influences(problem_data.scheme)

    solver = Solver()
    satisfy_composition(solver, experiment, problem_data)
            
    for key in problem_data.scheme.statements:
        for st in problem_data.scheme.statements[key]:
            solver.add(satisfy_statement(experiment, key, st))
            
    hypothesis = problem_data.hypothesis
    key = hypothesis.variableFrom, hypothesis.variableTo
    solver.add(Not(satisfy_statement(experiment, key, hypothesis)))
    
    def solve() -> Optional[Points]:
        result = solver.check()
        if result != sat:
            return None

        model = solver.model()
        return extract_model(problem_data, experiment, model)
    return solve
                    
                    
def extract_model(problem_data: ProblemData, experiment, model) -> Points:
    result: dict[str, dict[str, list[tuple[RatNumRef, RatNumRef]]]] = defaultdict(lambda: defaultdict(list))

    x = Real('x')
    for a in problem_data.scheme.variables:
        for b in problem_data.scheme.order[a]:
            f_interp = model.get_interp(experiment[(a, b)])
            val = f_interp.else_value()
            val_sub = substitute_vars(val, x)
            bounds = collect_bound_values(val_sub, set())
            
            def cast(num):
                if type(num) in [float, int]:
                    return float(num)
                return num.numerator_as_long() / num.denominator_as_long()
            
            for bound in sorted(bounds, key=cast):
                fn_value = model.evaluate(experiment[(a, b)](bound), model_completion=True)
                assert type(fn_value) == RatNumRef, 'Wrongly typed value found'
                result[a][b].append( (bound, fn_value) )
                
    return cleanup_points(result, problem_data, model, experiment)


def cleanup_points(points, problem_data, model, experiment):
    final: Points = {
        a: {
            b: [
                Point(
                    x.numerator_as_long() / x.denominator_as_long(),
                    y.numerator_as_long() / y.denominator_as_long()
                )
                for x, y in points[a][b]
            ]
            for b in points[a]
        }
        for a in points
    }
    
    for a in final:
        sts_bounds = poi.boundaries(problem_data, a)
        for b in final[a]:
            fn_value_right = model.evaluate(experiment[(a, b)](sts_bounds[-1]), model_completion=True)
            fn_value_left = model.evaluate(experiment[(a, b)](sts_bounds[0]), model_completion=True)
            
            point_left = Point(
                sts_bounds[0],
                fn_value_left.numerator_as_long() / fn_value_left.denominator_as_long()
            )
            point_right = Point(
                sts_bounds[-1],
                fn_value_right.numerator_as_long() / fn_value_right.denominator_as_long()
            )

            if point_left not in final[a][b]:
                final[a][b].append(point_left)

            if point_right not in final[a][b]:
                final[a][b].append(point_right)
            
            final[a][b] = [p for p in final[a][b] if p.x >= sts_bounds[0] and p.x <= sts_bounds[-1]] 
            final[a][b].sort()
    return final
        

def collect_bound_values(expr, bounds: set):
    if not is_app_of(expr, Z3_OP_ITE):
        return bounds

    cond = expr.arg(0)
    collect_bounds_in_cond(cond, bounds)

    then_branch = expr.arg(1)
    else_branch = expr.arg(2)

    collect_bound_values(then_branch, bounds)
    collect_bound_values(else_branch, bounds)
    return bounds
    

def collect_bounds_in_cond(cond, bounds: set):
    num_args = cond.num_args()

    for i in range(num_args):
        arg = cond.arg(i)
        if type(arg) == RatNumRef:
            bounds.add(arg)
            continue
        collect_bounds_in_cond(arg, bounds)
        
    
def create_influences(scheme: Scheme):
    Sort = RealSort()
    return {
        (a, b): Function(f'F_{{{a}, {b}}}', Sort, Sort)
        for a in scheme.variables
        for b in scheme.order[a]
    }
    

def satisfy_statement(experiment, key, st):
    return And(
        satisfy_range(st, experiment, key),
        satisfy_behaviour(st, experiment, key)
    )
    

def satisfy_composition(solver, experiment, problem_data):
    x = Real('x')

    for a in problem_data.scheme.variables:
        for b in problem_data.scheme.order[a]:
            for c in problem_data.scheme.order[b]:
                solver.add(
                    ForAll([x], experiment[(a, c)](x) == experiment[(b, c)](experiment[(a, b)](x)))
                )
        
        
def satisfy_behaviour(st, experiment, key):
    x = Real('x')
    y = Real('y')
    return ForAll(
        [x, y], 
        Implies(
            And( 
                x >= st.domain.start,
                x <= y,
                y <= st.domain.end
            ),
            behaviour_constraint(st, experiment, key, x, y)
        )
    )      
        

def satisfy_range(st, experiment, key):
    x = Real('x')
    return ForAll(
        [x], 
        Implies(
            And( 
                x >= st.domain.start,
                x <= st.domain.end
            ),
            And(
                experiment[key](x) >= st.range.start,
                experiment[key](x) <= st.range.end,
            )
        )
    )      
    
        
def behaviour_constraint(st, experiment, ab, x, y):
    if st.behaviour == Behaviour.MONO:
        return experiment[ab](x) <= experiment[ab](y)
    if st.behaviour == Behaviour.ANTI:
        return experiment[ab](x) >= experiment[ab](y)
    if st.behaviour == Behaviour.CONST:
        return experiment[ab](x) == experiment[ab](y)
    return True
    
