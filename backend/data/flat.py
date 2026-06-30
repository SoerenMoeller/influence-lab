from math import pi, sin


from model.behaviour import Behaviour
from model.scheme import Scheme
from model.interval import Interval
from model.problem_data import ProblemData
from model.statement import LongStatement
import data.exp_to_scheme as ets


def get_problem(size_domain: int, range_offset: float) -> ProblemData:
    parameters = ets.BenchmarkParameters(
        definition_start=0,
        definition_end=2 * pi,
        overlap_area=0.3,
        statement_width=2 * pi / size_domain,
        range_offset=range_offset,
        size_domain=size_domain,
    )

    pts = list(ets.sample_points(parameters, sin))
    fn = ets.points_to_piecewise_linear(pts)
    statements = list(ets.collect_statements(parameters, fn, pts, "x", "y"))

    return ProblemData(
        [Scheme(statements)],
        LongStatement("x", Interval(0, 2 * pi), Behaviour.CONST, Interval(-1, 1), "y"),
    )


if __name__ == "__main__":
    print("hi")
    get_problem(10, 10)
