from math import pi, sin

import data.exp_to_scheme as ets
from model.behaviour import Behaviour
from model.interval import Interval
from model.problem_data import ProblemData
from model.scheme import Scheme
from model.statement import LongStatement


def get_problem(size_domain: int, precision_max: float, precision_min: float, chain_length: int) -> ProblemData:
    parameters = ets.BenchmarkParameters(
        definition_start=-2 * pi - 1,
        definition_end=2 * pi + 1,
        overlap_area=0.3,
        statement_width=4 * pi / size_domain,
        range_offset=precision_max, # tmp
        size_domain=size_domain,
    )

    statements = []
    for i in range(chain_length):
        pts = list(ets.sample_points(parameters, lambda x: 2*pi*sin(x)))
        fn = ets.points_to_piecewise_linear(pts)
        statements.extend(ets.collect_statements(parameters, fn, pts, f"x{i}", f"x{i + 1}"))

    for i in range(2, chain_length):
        def fn(x):
            for _ in range(i):
                x = 2 * pi * sin(x)
            return x
        parameters.range_offset = precision_min + (precision_max - precision_min) * (chain_length - i) / chain_length
        pts = list(ets.sample_points(parameters, fn))
        fn = ets.points_to_piecewise_linear(pts)
        statements.extend(ets.collect_statements(parameters, fn, pts, f"x0", f"x{i}"))

    return ProblemData(
        Scheme(statements),
        LongStatement("x0", Interval(0, 2 * pi), Behaviour.CONST, Interval(-1, 1), f"x{chain_length - 1}"),
    )


if __name__ == "__main__":
    get_problem(10, 2, 2, 3)
    
