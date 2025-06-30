from typing import NamedTuple

from model.interval import Interval
from model.behaviour import Behaviour

class Statement(NamedTuple):
    variableFrom: str
    domain: Interval
    behavior: Behaviour
    range : Interval
    variableTo: str
    
