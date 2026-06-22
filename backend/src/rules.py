from typing import Optional
from model.interval import Interval
from model.statement import Statement
from model.behaviour import Behaviour
import model.behaviour as bhv


def overlap(st: Statement, iv: Interval) -> bool:
    l, u = iv.to_tuple()
    s_l, s_u = st.domain.to_tuple()
    return s_l >= l and s_u > l and s_l < u


def overlapping(sts: list[Statement], iv: Interval) -> list[Statement]:
    return [st for st in sts if overlap(st, iv)]


def contains(st: Statement, iv: Interval) -> bool:
    l, u = iv.to_tuple()
    s_l, s_u = st.domain.to_tuple()
    return l >= s_l and u <= s_u


def containing(sts: list[Statement], iv: Interval) -> list[Statement]:
    return [st for st in sts if contains(st, iv)]


def intersect(sts: list[Statement], domain: Interval) -> Optional[Statement]:
    if not sts:
        return None

    range_ = Interval(
        max(st.range.start for st in sts), min(st.range.end for st in sts)
    )

    behaviour = bhv.meet(st.behaviour for st in sts)

    return Statement(domain, behaviour, range_)


def join(sts: list[Statement]) -> Optional[Statement]:
    if not sts:
        return None

    domain = Interval(
        min(st.domain.start for st in sts), max(st.domain.end for st in sts)
    )

    behaviour = bhv.join(st.behaviour for st in sts)

    range_ = Interval(
        min(st.range.start for st in sts), max(st.range.end for st in sts)
    )

    return Statement(domain, behaviour, range_)


def left_rule(st1: Statement, st2: Statement) -> Optional[Statement]:
    st1_l, st1_u = st1.range.to_tuple()
    st2_l, st2_u = st2.range.to_tuple()

    new_rng = st1.range
    match st1.behaviour:
        case Behaviour.MONO:
            new_rng = Interval(st1_l, min(st1_u, st2_u))
        case Behaviour.ANTI:
            new_rng = Interval(max(st1_l, st2_l), st1_u)
        case Behaviour.CONST:
            new_rng = Interval(max(st1_l, st2_l), min(st1_u, st2_u))

    if new_rng == st1.range:
        return None
    return Statement(st1.domain, st1.behaviour, new_rng)


def right_rule(st1: Statement, st2: Statement) -> Optional[Statement]:
    st1_l, st1_u = st1.range.to_tuple()
    st2_l, st2_u = st2.range.to_tuple()

    new_rng = st2.range
    match st2.behaviour:
        case Behaviour.MONO:
            new_rng = Interval(max(st1_l, st2_l), st2_u)
        case Behaviour.ANTI:
            new_rng = Interval(st2_l, min(st1_u, st2_u))
        case Behaviour.CONST:
            new_rng = Interval(max(st1_l, st2_l), min(st1_u, st2_u))

    if new_rng == st2.range:
        return None
    return Statement(st2.domain, st2.behaviour, new_rng)


def comp_rule(
    st: Statement, sts: list[Statement], varA: str, varB: str, varC: str
) -> Optional[Statement]:
    overlapping_sts = [s for s in sts if overlap(s, st.domain)]
    joined = join(overlapping_sts)

    if joined is None:
        return None

    new_rng = joined.range
    new_behaviour = bhv.compose2(st.behaviour, joined.behaviour)

    return Statement(st.domain, new_behaviour, new_rng)

