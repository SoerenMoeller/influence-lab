from collections.abc import Iterable
from enum import Enum
from functools import reduce


class Behaviour(Enum):
    MONO = "mono"
    ANTI = "anti"
    CONST = "const"
    ARB = "arb"

    @staticmethod
    def serialise(behaviour) -> str:
        return behaviour.value

    @staticmethod
    def deserialise(data: str) -> "Behaviour":
        return Behaviour(data)


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


def compose2(beh1: Behaviour, beh2: Behaviour) -> Behaviour:
    if beh1 == Behaviour.CONST or beh2 == Behaviour.CONST:
        return Behaviour.CONST
    if beh1 == Behaviour.ARB or beh2 == Behaviour.ARB:
        return Behaviour.ARB
    if beh1 == Behaviour.MONO and beh2 == Behaviour.MONO:
        return Behaviour.MONO
    if beh1 == Behaviour.ANTI and beh2 == Behaviour.ANTI:
        return Behaviour.MONO
    else:
        return Behaviour.ANTI


def compose(behaviours: Iterable[Behaviour]) -> Behaviour:
    return reduce(compose2, behaviours, Behaviour.MONO)
