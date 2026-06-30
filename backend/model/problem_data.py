from dataclasses import dataclass
from model.scheme import Scheme
from model.statement import LongStatement


@dataclass
class ProblemData:
    schemeVersions: list[Scheme]
    hypothesis: LongStatement | None

    def serialise(self) -> dict:
        obj = {
            "schemeVersions": [scheme.serialise() for scheme in self.schemeVersions],
        }

        if self.hypothesis is not None:
            obj["hypothesis"] = self.hypothesis.serialise()

        return obj

    @staticmethod
    def deserialise(data: dict) -> "ProblemData":
        scheme = [Scheme.deserialise(scheme) for scheme in data["schemeVersions"]]
        hypothesis = (
            LongStatement.deserialise(data["hypothesis"])
            if "hypothesis" in data
            else None
        )

        return ProblemData(scheme, hypothesis)
