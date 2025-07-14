from typing import NamedTuple

from model.interval import Interval, deserialize_interval, serialize_interval
from model.behaviour import Behaviour, deserialize_behaviour, serialize_behaviour


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
    
    
def serialise_statement(st: Statement) -> dict:
    return {
        "domain": serialize_interval(st.domain),
        "behaviour": serialize_behaviour(st.behaviour),
        "range": serialize_interval(st.range)
    }


def deserialise_statement(data: dict) -> Statement:
    return Statement(
        domain=deserialize_interval(data["domain"]),
        behaviour=deserialize_behaviour(data["behaviour"]),
        range_=deserialize_interval(data["range"])
    )


def serialise_long_statement(statement: LongStatement) -> dict:
    return {
        'variableFrom': statement.variableFrom,
        'domain': {
            'start': statement.domain.start,
            'end': statement.domain.end,
        },
        'behaviour': serialize_behaviour(statement.behaviour),
        'range': {
            'start': statement.range.start,
            'end': statement.range.end,
        },
        'variableTo': statement.variableTo 
    }
    
    
def deserialise_long_statement(data: dict) -> LongStatement:
    return LongStatement(
        data['variableFrom'],
        Interval(
            data['domain']['start'],
            data['domain']['end']
        ),
        Behaviour(data['behaviour']),
        Interval(
            data['range']['start'],
            data['range']['end']
        ),
        data['variableTo']
    ) 
    