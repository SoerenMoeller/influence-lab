from dataclasses import dataclass
from model.scheme import Scheme, deserialise_scheme, serialise_scheme
from model.statement import LongStatement, deserialise_long_statement, serialise_long_statement


@dataclass
class ProblemData:
    scheme: Scheme
    hypothesis: LongStatement
    

def serialise_problem_data(problemData: ProblemData) -> dict:
    return {
        'scheme': serialise_scheme(problemData.scheme),
        'hypothesis': serialise_long_statement(problemData.hypothesis) 
    }


def deserialise_problem_data(data: dict) -> ProblemData:
    scheme = deserialise_scheme(data['scheme'])
    hypothesis = deserialise_long_statement(data['hypothesis'])
    
    return ProblemData(scheme, hypothesis)


