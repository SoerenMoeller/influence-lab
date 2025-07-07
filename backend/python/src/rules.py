from typing import Optional
from model.interval import Interval
from model.statement import Statement
from model.behaviour import Behaviour
import model.behaviour as bhv


def overlap(st: Statement, iv: Interval) -> bool:
    l, u = iv.to_tuple()
    s_l, s_u = st.domain.to_tuple()
    return s_l < u and s_u > l


def overlapping(sts: list[Statement], iv: Interval) -> list[Statement]:
    return [st for st in sts if overlap(st, iv)]


def intersect(sts: list[Statement], domain: Interval) -> Optional[Statement]:
    if not sts:
        return None
    
    range_ = Interval(
        max(st.range.start for st in sts),
        min(st.range.end for st in sts)
    ) 
    
    behaviour = bhv.meet(st.behaviour for st in sts)
    
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
        
        
# leftRule :: Statement -> Statement -> Statement
# leftRule st1 st2 =
#   case behaviour st1 of
#     MONO -> Statement (domain st1) MONO (mkInterval l (min u u'))
#     ANTI -> Statement (domain st1) ANTI (mkInterval (max l l') u)
#     CONST -> Statement (domain st1) CONST (mkInterval (max l l') (min u u'))
#     ARB -> st1
#   where
#     (l, u) = (start . range $ st1, end . range $ st1)
#     (l', u') = (start . range $ st2, end . range $ st2)