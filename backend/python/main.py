import z3

from model.statement import Statement
from model.interval import Interval
from model.behaviour import Behaviour 
from model.scheme import Scheme
import model.variable as var

scheme = Scheme([
    Statement('a', Interval(0, 1), Behaviour.ANTI, Interval(0, 2), 'b'),       
    Statement('b', Interval(0, 1), Behaviour.MONO, Interval(0, 2), 'd'),
    Statement('b', Interval(1, 2), Behaviour.MONO, Interval(0, 2), 'd'),
    Statement('a', Interval(0, 1), Behaviour.CONST, Interval(0, 1), 'd'),
    Statement('a', Interval(0, 1), Behaviour.MONO, Interval(0, 2), 'c'),
    Statement('c', Interval(0, 2), Behaviour.MONO, Interval(0, 2), 'd')
])
print(scheme)

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
