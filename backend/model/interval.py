from dataclasses import dataclass

@dataclass(frozen=True)
class Interval:
    start: float
    end:   float
    
    def to_tuple(self):
        return (self.start, self.end)
    
    def __post_init__(self):
        if self.start > self.end:
            raise ValueError("start must not exceed end")
        
    def __str__(self):
        return f'[{self.start}, {self.end}]'
    

def subinterval(iv1: Interval, iv2: Interval) -> bool:
    return iv1.start >= iv2.start and iv1.end <= iv2.end


def serialize_interval(iv: Interval) -> dict:
    return {"start": iv.start, "end": iv.end}


def deserialize_interval(data: dict) -> Interval:
    return Interval(data["start"], data["end"])
