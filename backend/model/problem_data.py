from dataclasses import dataclass
from model.scheme import Scheme
from model.statement import LongStatement

@dataclass
class ProblemData:
    scheme: Scheme
    hypothesis: LongStatement