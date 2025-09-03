from math import pi, sin

import data.exp_to_scheme as ets
from model.behaviour import Behaviour
from model.interval import Interval
from model.problem_data import ProblemData
from model.scheme import Scheme
from model.statement import LongStatement


def get_problem(size_domain: int, range_offset: float, chain_lendth: int) -> ProblemData:
    parameters = ets.BenchmarkParameters(
        definition_start=-2 * pi - 1,
        definition_end=2 * pi + 1,
        overlap_area=0.3,
        statement_width=4 * pi / size_domain,
        range_offset=range_offset,
        size_domain=size_domain,
    )

    statements = []
    for i in range(chain_lendth):
        pts = list(ets.sample_points(parameters, lambda x: 2*pi*sin(x)))
        fn = ets.points_to_piecewise_linear(pts)
        statements.extend(ets.collect_statements(parameters, fn, pts, f"x{i}", f"x{i + 1}"))

    return ProblemData(
        Scheme(statements),
        LongStatement("x0", Interval(0, 2 * pi), Behaviour.CONST, Interval(-1, 1), f"x{chain_lendth}"),
    )


if __name__ == "__main__":
    get_problem(10, 10, 3)
    
