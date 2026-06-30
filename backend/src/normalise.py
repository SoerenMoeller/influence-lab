from model.interval import Interval
from model.statement import Statement
from model.problem_data import ProblemData
from model.scheme import Scheme
import model.scheme as scheme
import src.rules as rules


def normalise(problem_data: ProblemData) -> ProblemData:
    if len(problem_data.schemeVersions) != 1:
        raise ValueError("Only one scheme version is allowed for normalisation.")

    current_scheme = problem_data.schemeVersions[0]
    current_scheme.statements = {
        (a, b): normalise_subscheme(problem_data, current_scheme, a, b)
        for (a, b) in current_scheme.statements
    }
    return problem_data


def normalise_subscheme(
    problem_data: ProblemData, current_scheme: Scheme, var_from: str, var_to: str
) -> list[Statement]:
    statements = current_scheme.statements[(var_from, var_to)]
    transforms = [overlap_free, minimal_height]

    for fn in transforms:
        statements = fn(problem_data, var_from, statements)
        print(f"After {fn.__name__}:\n{statements}\n")

    return statements


def overlap_free(
    problem_data: ProblemData,
    current_scheme: Scheme,
    var_from: str,
    statements: list[Statement],
) -> list[Statement]:
    bounds = sorted(scheme.boundary_points(current_scheme)[var_from])

    result = []
    for i in range(len(bounds)):
        x = bounds[i]
        y = bounds[i]

        overlapping = rules.containing(statements, Interval(x, y))
        print(x, y, overlapping)
        st = rules.intersect(overlapping, Interval(x, y))

        if st is not None:
            result.append(st)

        if not i + 1 < len(bounds):
            continue

        y = bounds[i + 1]
        overlapping = rules.containing(statements, Interval(x, y))
        st = rules.intersect(overlapping, Interval(x, y))

        if st is not None:
            result.append(st)
    return result


def minimal_height(
    problem_data: ProblemData, var_from: str, sts: list[Statement]
) -> list[Statement]:
    i = 0
    while 0 <= i < len(sts) - 1:
        go_left = False

        assert (
            sts[i].domain.end == sts[i + 1].domain.start
        ), "Gap found while normalising"

        new_st = rules.left_rule(sts[i], sts[i + 1])
        if new_st is not None:
            go_left = True
            sts[i] = new_st

        new_st = rules.right_rule(sts[i], sts[i + 1])
        if new_st is not None:
            go_left = True
            sts[i + 1] = new_st

        if go_left:
            i -= 1
        else:
            i += 1

    return sts
