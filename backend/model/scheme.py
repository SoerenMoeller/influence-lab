from collections import defaultdict
from typing_extensions import override
from model.statement import Statement, LongStatement, deserialise_statement, serialise_statement


class Scheme:
    def __init__(self, statements: list[LongStatement]):
        self.statements: dict[tuple[str, str], list[Statement]] = defaultdict(lambda: list())
        self.variables: set[str] = set()
        self.order: dict[str, set[str]] = defaultdict(lambda: set())

        for statement in statements:
            self.variables.add(statement.variableFrom)
            self.variables.add(statement.variableTo)
            self.order[statement.variableFrom].add(statement.variableTo)
            self.statements[(statement.variableFrom, statement.variableTo)].append(Statement(statement.domain, statement.behaviour, statement.range))

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
        result = ''
        for a, b in self.statements:
            result += f'C_{{{a}, {b}}}:\n'
            for st in self.statements[(a, b)]:
                result += f'    {str(st)}\n'

        return result


def serialise_scheme(scheme: Scheme) -> dict:
    return {
        "variables": sorted(scheme.variables),
        "order": [
            {
                "variableFrom": var_from,
                "variableTos": sorted(list(var_tos))
            }
            for var_from, var_tos in scheme.order.items()
        ],
        "statements": [
            {
                "variableFrom": var_from,
                "variableTo": var_to,
                "statements": [serialise_statement(st) for st in scheme.statements[(var_from, var_to)]]
            }
            for var_from, var_to in scheme.statements
        ]
    }


def deserialise_scheme(data: dict) -> Scheme:
    scheme = Scheme([])
    scheme.variables = set(data['variables'])

    for entry in data['order']:
        var_from = entry['variableFrom']

        for var_to in entry['variableTos']:
            scheme.order[var_from].add(var_to)

    scheme.statements
    for entry in data['statements']:
        scheme.statements[(entry['variableFrom'], entry['variableTo'])] = \
            [deserialise_statement(e) for e in entry['statements']]

    return scheme
