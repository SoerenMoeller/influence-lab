from typing import NamedTuple

from model.interval import Interval
from model.behaviour import Behaviour


class LongStatement(NamedTuple):
    variableFrom: str
    domain: Interval
    behaviour: Behaviour
    range : Interval
    variableTo: str
    

class Statement(NamedTuple):
    domain: Interval
    behaviour: Behaviour
    range : Interval