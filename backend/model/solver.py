from enum import Enum


class Solver(Enum):
    SAT = 'sat'
    ARRAY = 'array'
    INTEGER = 'integer'
    UNINTEPRETED_FUNCTIONS = 'uninterpreted'