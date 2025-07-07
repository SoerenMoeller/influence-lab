from collections import defaultdict
from model.statement import Statement, LongStatement


class Scheme:
    def __init__(self, statements: list[LongStatement]):
        self.statements: dict[tuple[str, str], set[Statement]] = defaultdict(lambda: set())
        self.variables: set[str] = set() 
        self.order: dict[str, set[str]] = defaultdict(lambda: set())

        for statement in statements:
            self.variables.add(statement.variableFrom)
            self.variables.add(statement.variableTo)
            self.order[statement.variableFrom].add(statement.variableTo)
            self.statements[(statement.variableFrom, statement.variableTo)].add(Statement(statement.domain, statement.behaviour, statement.range))

        for k in self.variables:
            for i in self.variables:
                if k in self.order[i]:
                    self.order[i].update(self.order[k])
                    
    def __str__(self):
        return str(self.statements)

        
