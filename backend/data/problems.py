from model.behaviour import Behaviour
from model.interval import Interval
from model.problem_data import ProblemData
from model.scheme import Scheme
from model.statement import LongStatement


def get_problems() -> list[ProblemData]: 
    return [
        ProblemData(
            Scheme([
                LongStatement('a', Interval(0, 1), Behaviour.ANTI, Interval(0, 2), 'b'),       
                LongStatement('b', Interval(0, 1), Behaviour.MONO, Interval(0, 2), 'd'),
                LongStatement('b', Interval(1, 2), Behaviour.MONO, Interval(0, 2), 'd'),
                LongStatement('a', Interval(0, 1), Behaviour.CONST, Interval(0, 1), 'd'),
                LongStatement('a', Interval(0, 1), Behaviour.MONO, Interval(0, 2), 'c'),
                LongStatement('c', Interval(0, 2), Behaviour.MONO, Interval(0, 2), 'd')
            ]),
            LongStatement('a', Interval(0, 1), Behaviour.MONO, Interval(0, 0.5), 'd')
        ),
        ProblemData(
            Scheme([
                LongStatement('a', Interval(0, 2), Behaviour.ANTI, Interval(3, 3.5), 'b'),
                LongStatement('a', Interval(2, 3.3), Behaviour.ANTI, Interval(2.1, 3.2), 'b'),
                LongStatement('a', Interval(3, 4.5), Behaviour.ANTI, Interval(1.4, 2.2), 'b'),
                LongStatement('a', Interval(4, 5.1), Behaviour.ANTI, Interval(1.2, 2), 'b'),
                LongStatement('a', Interval(5, 7), Behaviour.MONO, Interval(1.1, 1.9), 'b'),
                LongStatement('a', Interval(7, 8), Behaviour.CONST, Interval(1.7, 3), 'b'),
                LongStatement('a', Interval(7.9, 9), Behaviour.ANTI, Interval(1, 2), 'b'),
                LongStatement('a', Interval(8.6, 10.8), Behaviour.MONO, Interval(1.5, 1.8), 'b'),
                LongStatement('a', Interval(8.6, 10.7), Behaviour.ANTI, Interval(1.6, 2.2), 'b'),
                LongStatement('a', Interval(10, 11), Behaviour.ANTI, Interval(1.3, 1.9), 'b')
            ]),
            LongStatement('a', Interval(7, 9), Behaviour.CONST, Interval(1, 2), 'b')
        ),
        ProblemData(
            Scheme([
                LongStatement('a', Interval(0, 1), Behaviour.ANTI, Interval(0, 1), 'b'),
                LongStatement('b', Interval(0, 1), Behaviour.MONO, Interval(0, 1), 'c'),
                LongStatement('a', Interval(0, 1), Behaviour.CONST, Interval(0, 1), 'c'),
                LongStatement('b', Interval(0, 1), Behaviour.MONO, Interval(0, 1), 'd'),
                LongStatement('a', Interval(0, 1), Behaviour.ANTI, Interval(0, 1), 'd'),
                # LongStatement('b', Interval(-1, 0), Behaviour.MONO, Interval(-0.5, 0), 'c'),
                # LongStatement('b', Interval(1, 2), Behaviour.MONO, Interval(0.5, 1.5), 'c'),
            ]),
            LongStatement('a', Interval(0, 1), Behaviour.CONST, Interval(0, 1), 'd'),
        )
    ]
    