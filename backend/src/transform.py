from collections import defaultdict
from model.problem_data import ProblemData
from model.scheme import Scheme
from model.statement import LongStatement, Statement
from model.interval import Interval
from model.behaviour import Behaviour
import json


def serialize_interval(iv: Interval) -> dict:
    return {"start": iv.start, "end": iv.end}


def deserialize_interval(data: dict) -> Interval:
    return Interval(data["start"], data["end"])


def serialize_behaviour(beh: Behaviour) -> str:
    return beh.value


def deserialize_behaviour(val: str) -> Behaviour:
    return Behaviour(val)


def serialize_statement(st: Statement) -> dict:
    return {
        "domain": serialize_interval(st.domain),
        "behaviour": serialize_behaviour(st.behaviour),
        "range": serialize_interval(st.range)
    }


def deserialize_statement(data: dict) -> Statement:
    return Statement(
        domain=deserialize_interval(data["domain"]),
        behaviour=deserialize_behaviour(data["behaviour"]),
        range_=deserialize_interval(data["range"])
    )


def serialize_scheme(scheme: Scheme) -> dict:
    return {
        "variables": sorted(scheme.variables),
        "order": [
            {
                "variableFrom": var_from,
                "variableTos": sorted(list(var_tos))
            }
            for var_from, var_tos in scheme.order.items()
        ],
        "statements": [
            {
                "variableFrom": var_from,
                "variableTo": var_to,
                "statements": [serialize_statement(st) for st in scheme.statements[(var_from, var_to)]]
            }
            for var_from, var_to in scheme.statements
        ]
    }
    
    
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
    

def serialise_problem_data(problemData: ProblemData) -> dict:
    return {
        'scheme': serialize_scheme(problemData.scheme),
        'hypothesis': serialise_long_statement(problemData.hypothesis) 
    }


def deserialise_problem_data(data: dict) -> ProblemData:
    scheme = deserialize_scheme(data['scheme'])
    hypothesis = deserialise_long_statement(data['hypothesis'])
    
    return ProblemData(scheme, hypothesis)


def deserialize_scheme(data: dict) -> Scheme:
    scheme = Scheme([])
    scheme.variables = set(data['variables'])

    for entry in data['order']:
        var_from = entry['variableFrom']

        for var_to in entry['variableTos']:
            scheme.order[var_from].add(var_to)
            
    scheme.statements 
    for entry in data['statements']:
        scheme.statements[(entry['variableFrom'], entry['variableTo'])] = \
            [deserialize_statement(e) for e in entry['statements']]

    return scheme