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
    for a, b in current_scheme.statements:
        current_scheme.statements[(a, b)] = normalise_subscheme(current_scheme, a, b)

    return problem_data


def normalise_subscheme(
    current_scheme: Scheme, var_from: str, var_to: str
) -> list[Statement]:
    bounds: list[float] = sorted(scheme.boundary_points(current_scheme)[var_from])

    statements = current_scheme.statements[(var_from, var_to)]
    # ToDo: Remove gaps
    statements = overlap_free(statements, bounds)
    statements = minimal_height(statements)

    return statements


def overlap_free(statements: list[Statement], bounds: list[float]) -> list[Statement]:
    result = []
    for i in range(len(bounds)):
        x = bounds[i]
        y = bounds[i]

        overlapping = rules.containing(statements, Interval(x, y))
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


def minimal_height(statements: list[Statement]) -> list[Statement]:
    changes = True
    while changes:
        changes = False

        for i in range(len(statements) - 1):
            current = statements[i]
            next_st = statements[i + 1]

            new_st = rules.left_rule(current, next_st)
            if new_st is not None:
                statements[i] = new_st
                changes = True

            new_st = rules.right_rule(current, next_st)
            if new_st is not None:
                statements[i + 1] = new_st
                changes = True

        for i in range(len(statements), -1):
            current = statements[i]
            next_st = statements[i - 1]

            new_st = rules.left_rule(current, next_st)
            if new_st is not None:
                statements[i] = new_st
                changes = True

            new_st = rules.right_rule(current, next_st)
            if new_st is not None:
                statements[i + 1] = new_st
                changes = True

    return statements
