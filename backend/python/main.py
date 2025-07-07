import z3

from model.statement import Statement, LongStatement
from model.interval import Interval
from model.behaviour import Behaviour 
from model.scheme import Scheme
import model.variable as vbl
import src.points as points
import src.normalise as normalise

scheme = Scheme([
    LongStatement('a', Interval(0, 1), Behaviour.ANTI, Interval(0, 2), 'b'),       
    LongStatement('b', Interval(0, 1), Behaviour.MONO, Interval(0, 2), 'd'),
    LongStatement('b', Interval(1, 2), Behaviour.MONO, Interval(0, 2), 'd'),
    LongStatement('a', Interval(0, 1), Behaviour.CONST, Interval(0, 1), 'd'),
    LongStatement('a', Interval(0, 1), Behaviour.MONO, Interval(0, 2), 'c'),
    LongStatement('c', Interval(0, 2), Behaviour.MONO, Interval(0, 2), 'd')
])
scheme2 = Scheme([
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
])    
    
# print(scheme2)
print(normalise.normalise(scheme2))
# normalise.normalise(scheme2)

# print(points.boundaries(scheme, 'a'))
# print(points.dist_tp2(scheme, 'a', 'b', 0, 1))

# Create solver instance
s = z3.Solver()

# Create some integer variables
x = z3.Int('x')
y = z3.Int('y')

# Add constraints: x + y = 10, x > 0, y > 0
s.add(x + y == 10, x > 0, y > 0)

# Check satisfiability
if s.check() == z3.sat:
    model = s.model()
    print(f"x = {model[x]}")
    print(f"y = {model[y]}")
else:
    print("No solution")
