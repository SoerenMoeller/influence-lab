from dataclasses import dataclass, field
from collections import defaultdict
from model.statement import Statement

@dataclass
class Scheme:
    statements: list[Statement]
    variables: set[str] = field(init=False)
    order: dict[str, set[str]] = field(init=False)

    def __post_init__(self):
        self.variables = set()
        self.order = defaultdict(lambda: set())
        
        for statement in self.statements:
            self.variables.add(statement.variableFrom)
            self.variables.add(statement.variableTo)
            self.order[statement.variableFrom].add(statement.variableTo)

        for k in self.variables:
            for i in self.variables:
                if k in self.order[i]:
                    self.order[i].update(self.order[k])

        
