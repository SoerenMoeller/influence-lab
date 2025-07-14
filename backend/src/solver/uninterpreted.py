# from collections import defaultdict
# import json
# from z3 import *
# from model.scheme import Scheme
# from model.behaviour import Behaviour
# from model.problem_data import ProblemData


#     # problem_data = schemes[0]
#     # result: dict[str, dict[str, list]] = solver.solve(problem_data)
    
#     # if not result:
#     #     return 1
    
#     # # print('<<<RESULT>>>')
#     # # print(json.dumps(result))

#     # print(result)
#     # scheme = problem_data.scheme
    
#     # experiment = defaultdict(lambda: defaultdict(list))
#     # for a in scheme.variables:
#     #     for b in vbl.post(scheme, a):
#     #         experiment[a][b] = result[a][b]
            
#     # print(experiment)

#     # var_queue = [var for var in scheme.variables if vbl.is_minimal(scheme, var)]
#     # while var_queue:
#     #     var = var_queue[0]
#     #     var_queue = var_queue[1:]
#     #     print(var, vbl.post(scheme, var))
#     # print(var_queue)
   


# def solve(problem_data: ProblemData) -> dict[str, dict[str, list]]:
#     experiment = create_influences(problem_data.scheme)

#     solver = Solver()
#     satisfy_composition(solver, experiment)
            
#     for key in problem_data.scheme.statements:
#         for st in problem_data.scheme.statements[key]:
#             solver.add(satisfy_statement(experiment, key, st))
            
#     hypothesis = problem_data.hypothesis
#     key = hypothesis.variableFrom, hypothesis.variableTo
#     solver.add(Not(satisfy_statement(experiment, key, hypothesis)))
            
#     result = solver.check()
#     print('Result:', result)
#     if result != sat:
#         return {}

#     model = solver.model()
#     return extract_model(problem_data, experiment, model)
                    
                    
# def extract_model(problem_data: ProblemData, experiment, model) -> dict[str, dict[str, list]]:
#     result = defaultdict(lambda: defaultdict(list))

#     x = Real('x')
#     for a in problem_data.scheme.variables:
#         for b in problem_data.scheme.order[a]:
#             f_interp = model.get_interp(experiment[(a, b)])
#             val = f_interp.else_value()
#             val_sub = substitute_vars(val, x)
#             bounds = collect_bound_values(val_sub, set())
            
#             for bound in sorted(bounds):
#                 fn_value = model.evaluate(experiment[(a, b)](bound), model_completion=True)
#                 assert type(fn_value) == RatNumRef, 'Wrongly typed value found'
                     
#                 result[a][b].append({
#                     'x': bound,
#                     'y': fn_value.numerator_as_long() / fn_value.denominator_as_long()
#                 })
                
#     return result
#     # final = []
#     # for a in problem_data.scheme.variables:
#     #     for b in problem_data.scheme.order[a]:
#     #         final.append({
#     #             'variableFrom': a,
#     #             'variableTo': b,
#     #             'points': result[a][b]
#     #         })
    
#     # return final
        

# def collect_bound_values(expr, bounds: set):
#     if not is_app_of(expr, Z3_OP_ITE):
#         return bounds

#     cond = expr.arg(0)
#     collect_bounds_in_cond(cond, bounds)

#     then_branch = expr.arg(1)
#     else_branch = expr.arg(2)

#     collect_bound_values(then_branch, bounds)
#     collect_bound_values(else_branch, bounds)
#     return bounds
    

# def collect_bounds_in_cond(cond, bounds: set):
#     num_args = cond.num_args()

#     for i in range(num_args):
#         arg = cond.arg(i)
#         if type(arg) == RatNumRef:
#             bounds.add(arg.numerator_as_long() / arg.denominator_as_long())
#             continue
#         collect_bounds_in_cond(arg, bounds)
        
    
# def create_influences(scheme: Scheme):
#     Sort = RealSort()
#     return {
#         (a, b): Function(f'F_{{{a}, {b}}}', Sort, Sort)
#         for a in scheme.variables
#         for b in scheme.order[a]
#     }
    

# def satisfy_statement(experiment, key, st):
#     x = Real('x')
#     y = Real('y')
#     return And(
#         ForAll(
#             [x], 
#             Implies(
#                 And( 
#                     x >= st.domain.start,
#                     x <= st.domain.end
#                 ),
#                 And(
#                     experiment[key](x) >= st.range.start,
#                     experiment[key](x) <= st.range.end,
#                 )
#             )
#         ),
#         ForAll(
#             [x, y], 
#             Implies(
#                 And( 
#                     x >= st.domain.start,
#                     x <= y,
#                     y <= st.domain.end
#                 ),
#                 behaviour_constaint(st, experiment, key, x, y)
#             )
#         )      
#     )
    

# def satisfy_composition(solver, experiment):
#     x = Real('x')

#     for a, b in experiment:
#         for c, d in experiment:
#             if b != c:
#                 continue
            
#             solver.add(
#                 ForAll([x], experiment[(a, d)](x) == experiment[(b, d)](experiment[(a, b)](x)))
#             )
        
        
# def satisfy_behaviour(st, experiment, ab, x, y):
#     return ForAll(
#         [x, y], 
#         Implies(
#             And( 
#                 x >= st.domain.start,
#                 x <= y,
#                 y <= st.domain.end
#             ),
#             behaviour_constaint(st, experiment, ab, x, y)
#         )
#     )      
        

# def satisfy_range(st, experiment, ab, x):
#     return ForAll(
#         [x], 
#         Implies(
#             And( 
#                 x >= st.domain.start,
#                 x <= st.domain.end
#             ),
#             And(
#                 experiment[ab](x) >= st.range.start,
#                 experiment[ab](x) <= st.range.end,
#             )
#         )
#     )      
    
        
# def behaviour_constaint(st, experiment, ab, x, y):
#     if st.behaviour == Behaviour.MONO:
#         return experiment[ab](x) <= experiment[ab](y)
#     if st.behaviour == Behaviour.ANTI:
#         return experiment[ab](x) >= experiment[ab](y)
#     if st.behaviour == Behaviour.CONST:
#         return experiment[ab](x) == experiment[ab](y)
#     assert False, 'unreachable'
    