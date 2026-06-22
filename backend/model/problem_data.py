from dataclasses import dataclass
from model.scheme import Scheme
from model.statement import LongStatement


@dataclass
class ProblemData:
    scheme: Scheme
    hypothesis: LongStatement

    def serialise(self) -> dict:
        return {
            "scheme": self.scheme.serialise(),
            "hypothesis": self.hypothesis.serialise(),
        }

    @staticmethod
    def deserialise(data: dict) -> "ProblemData":
        scheme = Scheme.deserialise(data["scheme"])
        hypothesis = LongStatement.deserialise(data["hypothesis"])

        return ProblemData(scheme, hypothesis)
