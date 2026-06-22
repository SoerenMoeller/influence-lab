from collections import defaultdict
from typing_extensions import override
from model.serialisable import Serialisable
from model.statement import Statement, LongStatement


class Scheme(Serialisable):
    def __init__(self, statements: list[LongStatement]):
        self.statements: dict[tuple[str, str], list[Statement]] = defaultdict(
            lambda: list()
        )
        self.variables: set[str] = set()
        self.order: dict[str, set[str]] = defaultdict(lambda: set())

        for statement in statements:
            self.variables.add(statement.variableFrom)
            self.variables.add(statement.variableTo)
            self.order[statement.variableFrom].add(statement.variableTo)
            self.statements[(statement.variableFrom, statement.variableTo)].append(
                Statement(statement.domain, statement.behaviour, statement.range)
            )

        for k in self.variables:
            for i in self.variables:
                if k in self.order[i]:
                    self.order[i].update(self.order[k])

        for a in self.variables:
            for b in self.order[a]:
                if (a, b) not in self.statements:
                    self.statements[(a, b)] = []

    @override
    def __str__(self):
        result = ""
        for a, b in self.statements:
            result += f"C_{{{a}, {b}}}:\n"
            for st in self.statements[(a, b)]:
                result += f"    {str(st)}\n"

        return result

    def serialise(self) -> dict:
        return {
            "variables": sorted(self.variables),
            "order": [
                {"variableFrom": var_from, "variableTos": sorted(list(var_tos))}
                for var_from, var_tos in self.order.items()
            ],
            "statements": [
                {
                    "variableFrom": var_from,
                    "variableTo": var_to,
                    "statements": [
                        st.serialise() for st in self.statements[(var_from, var_to)]
                    ],
                }
                for var_from, var_to in self.statements
            ],
        }

    @staticmethod
    def deserialise(data: dict) -> "Scheme":
        scheme = Scheme([])
        scheme.variables = set(data["variables"])

        for entry in data["order"]:
            var_from = entry["variableFrom"]

            for var_to in entry["variableTos"]:
                scheme.order[var_from].add(var_to)

        scheme.statements
        for entry in data["statements"]:
            scheme.statements[(entry["variableFrom"], entry["variableTo"])] = [
                Statement.deserialise(e) for e in entry["statements"]
            ]

        return scheme


def boundary_points(scheme: Scheme) -> dict[str, set[float]]:
    points = defaultdict(set)

    for variable_from in scheme.variables:
        for variable_to in scheme.order[variable_from]:
            for statement in scheme.statements[(variable_from, variable_to)]:
                points[variable_from].add(statement.domain.start)
                points[variable_from].add(statement.domain.end)

                points[variable_to].add(statement.range.start)
                points[variable_to].add(statement.range.end)

    return points
