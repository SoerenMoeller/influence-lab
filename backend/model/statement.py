from dataclasses import dataclass
from model.interval import Interval
from model.behaviour import Behaviour
from model.serialisable import Serialisable


@dataclass(frozen=True)
class LongStatement(Serialisable):
    variableFrom: str
    domain: Interval
    behaviour: Behaviour
    range: Interval
    variableTo: str

    def serialise(self) -> dict:
        return {
            "variableFrom": self.variableFrom,
            "domain": {
                "start": self.domain.start,
                "end": self.domain.end,
            },
            "behaviour": Behaviour.serialise(self.behaviour),
            "range": {
                "start": self.range.start,
                "end": self.range.end,
            },
            "variableTo": self.variableTo,
        }

    @staticmethod
    def deserialise(data: dict) -> "LongStatement":
        return LongStatement(
            data["variableFrom"],
            Interval(data["domain"]["start"], data["domain"]["end"]),
            Behaviour.deserialise(data["behaviour"]),
            Interval(data["range"]["start"], data["range"]["end"]),
            data["variableTo"],
        )


class Statement(Serialisable):
    def __init__(self, domain, behaviour, range_):
        self.domain = domain
        self.behaviour = behaviour
        self.range = range_

    def __lt__(self, other):
        return (
            self.domain.start,
            self.domain.end,
            self.range.start,
            self.range.end,
        ) < (other.domain.start, other.domain.end, other.range.start, other.range.end)

    def __str__(self):
        return f"Statement({self.domain}, {self.behaviour}, {self.range})"

    def __repr__(self):
        return self.__str__()

    def serialise(self) -> dict:
        return {
            "domain": self.domain.serialise(),
            "behaviour": Behaviour.serialise(self.behaviour),
            "range": self.range.serialise(),
        }

    @staticmethod
    def deserialise(data: dict) -> "Statement":
        return Statement(
            domain=Interval.deserialise(data["domain"]),
            behaviour=Behaviour.deserialise(data["behaviour"]),
            range_=Interval.deserialise(data["range"]),
        )

