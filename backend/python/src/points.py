from model.scheme import Scheme
import model.variable as var

def boundaries(scheme: Scheme, variable: str) -> set[float]:
    ...

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
