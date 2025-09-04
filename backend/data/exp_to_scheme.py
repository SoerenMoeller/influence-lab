import bisect
from collections import namedtuple
from math import pi, sin
from typing import Iterator


from model.behaviour import Behaviour
from model.scheme import Scheme
from model.interval import Interval
from model.problem_data import ProblemData
from model.statement import LongStatement


BenchmarkParameters = namedtuple(
    "BenchmarkParameters",
    [
        "definition_start",
        "definition_end",
        "overlap_area",
        "statement_width",
        "range_offset",
        "size_domain",
    ],
)


def points_to_piecewise_linear(points: list[tuple[float, float]]):
    if not points:
        raise ValueError("points list cannot be empty")

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    def f(x: float) -> float:
        if x <= xs[0]:
            return ys[0]
        if x >= xs[-1]:
            return ys[-1]

        idx = bisect.bisect_left(xs, x)

        x1, y1 = points[idx - 1]
        x2, y2 = points[idx]

        if x1 == x2:
            return y1

        return y1 + (x - x1) * (y2 - y1) / (x2 - x1)

    return f


def collect_statements(
    parameters: BenchmarkParameters, fn, pts, variableFrom, variableTo
) -> Iterator[LongStatement]:
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        real_x1 = x1 - parameters.statement_width * (parameters.overlap_area / 2)
        real_x2 = x2 + parameters.statement_width * (parameters.overlap_area / 2)
        real_y1 = fn(real_x1)
        real_y2 = fn(real_x2)

        domain = Interval(real_x1, real_x2)

        behaviour = Behaviour.CONST
        if real_y1 < real_y2:
            behaviour = Behaviour.MONO
        elif real_y1 > real_y2:
            behaviour = Behaviour.ANTI

        range_ = Interval(
            min(real_y1, real_y2) - parameters.range_offset,
            max(real_y1, real_y2) + parameters.range_offset,
        )

        yield LongStatement(variableFrom, domain, behaviour, range_, variableTo)


def sample_points(parameters: BenchmarkParameters, fn) -> list[tuple[float, float]]:
    return [
        (x, fn(x))
        for x in [
            parameters.definition_start + i * parameters.statement_width
            for i in range(parameters.size_domain + 1)
        ]
    ]

