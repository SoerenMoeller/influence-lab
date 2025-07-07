from typing import NamedTuple

from model.interval import Interval
from model.behaviour import Behaviour


class LongStatement(NamedTuple):
    variableFrom: str
    domain: Interval
    behaviour: Behaviour
    range : Interval
    variableTo: str
    

class Statement:
    def __init__(self, domain, behaviour, range_):
        self.domain = domain
        self.behaviour = behaviour
        self.range = range_

    def __lt__(self, other):
        return (
            (self.domain.start, self.domain.end, self.range.start, self.range.end)
            <
            (other.domain.start, other.domain.end, other.range.start, other.range.end)
        )
    
    def __str__(self):
        return f'Statement({self.domain}, {self.behaviour}, {self.range})'
    
    def __repr__(self):
        return self.__str__()