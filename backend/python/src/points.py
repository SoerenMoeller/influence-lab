from model.scheme import Scheme
import model.variable as vbl

def boundaries(scheme: Scheme, variable: str) -> set[float]:
    statementsFrom = [st for var in vbl.post(variable, scheme) for st in scheme.statements[variable, var]]
    statementsTo = [st for var in vbl.pre(variable, scheme) for st in scheme.statements[var, variable]]

    bounds = set()
    for statement in statementsFrom:
        bounds.add(statement.domain.start)
        bounds.add(statement.domain.end)
    for statement in statementsTo:
        bounds.add(statement.range.start)
        bounds.add(statement.range.end)
        
    return bounds

def dist_tp(variable: str, x: float, y: float, scheme: Scheme) -> int:
    return sum(
        dist_tp2(variable, var2, x, y, scheme) for var2 in var.post(variable, scheme)
    )

def dist_tp2(var1: str, var2: str, x: float, y: float, scheme: Scheme) -> int:
    if var.is_maximal(var1, scheme):
        return 0

    result = 2
    # for i in range()
    # return result
