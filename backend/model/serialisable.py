from abc import ABC, abstractmethod
from typing import Any


class Serialisable(ABC):

    @abstractmethod
    def serialise(self: Any) -> Any:
        pass

    @staticmethod
    @abstractmethod
    def deserialise(data: Any) -> Any:
        pass
