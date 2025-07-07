from model.scheme import Scheme
from model.statement import LongStatement
from model.interval import Interval
from model.behaviour import Behaviour
import json


VAR_FROM = 'variableFrom'
DOMAIN = 'domain'
START = 'start'
END = 'end'
BEHAVIOUR = 'behaviour'
RANGE = 'range'
VAR_TO = 'variableTo'


def scheme_to_statement_list(scheme: Scheme) -> list[LongStatement]:
    result = []
    for a, b in scheme.statements:
        result.extend(
            [LongStatement(a, st.domain, st.behaviour, st.range, b) for st in scheme.statements[(a, b)]]
        ) 
        
    return result


def statement_list_to_json(statements: list[LongStatement]) -> str:
    return json.dumps([ 
        {
            VAR_FROM: st.variableFrom,
            DOMAIN: {
                START: st.domain.start,
                END: st.domain.end
            },
            BEHAVIOUR: st.behaviour.value,
            RANGE: {
                START: st.range.start,
                END: st.range.end
            },
            VAR_TO: st.variableTo
        }
        for st in statements
    ])
    

def json_to_statement_list(json_str: str) -> list[LongStatement]:
    statements = json.loads(json_str)
    return [
        LongStatement(
            data[VAR_FROM],
            Interval(data[DOMAIN][START], data[DOMAIN][END]),
            Behaviour(data[BEHAVIOUR]),
            Interval(data[RANGE][START], data[RANGE][END]),
            data[VAR_TO]
        ) 
        for data in statements
    ]