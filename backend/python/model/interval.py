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