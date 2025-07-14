from collections.abc import Iterable
from enum import Enum
from functools import reduce


class Behaviour(Enum):
    MONO  = "mono"
    ANTI  = "anti"
    CONST = "const"
    ARB   = "arb"
    
    
def serialize_behaviour(beh: Behaviour) -> str:
    return beh.value


def deserialize_behaviour(val: str) -> Behaviour:
    return Behaviour(val)


def less_equal(beh1: Behaviour, beh2: Behaviour) -> bool:
    if beh1 == Behaviour.CONST or beh2 == Behaviour.ARB:
        return True
    return beh1 == beh2


def join2(beh1: Behaviour, beh2: Behaviour) -> Behaviour:
    if less_equal(beh1, beh2):
        return beh2
    if less_equal(beh2, beh1):
        return beh1
    return Behaviour.ARB


def meet2(beh1: Behaviour, beh2: Behaviour) -> Behaviour:
    if less_equal(beh1, beh2):
        return beh1
    if less_equal(beh2, beh1):
        return beh2
    return Behaviour.CONST


def join(behaviours: Iterable[Behaviour]) -> Behaviour:
    return reduce(join2, behaviours, Behaviour.CONST)


def meet(behaviours: Iterable[Behaviour]) -> Behaviour:
    return reduce(meet2, behaviours, Behaviour.ARB)
