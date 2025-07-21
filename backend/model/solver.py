from enum import Enum


class Solver(Enum):
    SAT = 'sat'
    ARRAY = 'array'
    INTEGER = 'integer'
    INCREMENTAL = 'incremental'
    UNINTEPRETED_FUNCTIONS = 'uninterpreted'