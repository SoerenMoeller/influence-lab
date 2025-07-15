import bisect
from collections import defaultdict
from dataclasses import dataclass

from model.problem_data import ProblemData
import model.variable as vbl


@dataclass(order=True)
class Point:
    x: float
    y: float 
    

Points = dict[str, dict[str, list[Point]]]


def serialise_point(point: Point) -> dict:
    return {
        'x': point.x,
        'y': point.y
    }
    

def deserialise_point(data: dict) -> Point:
    return Point(data['x'], data['y'])


def serialise_points(points: Points) -> list:
    result = []
    for a in points:
        for b in points[a]:
            pts = [serialise_point(p) for p in points[a][b]] 
            result.append({
                'variableFrom': a,
                'variableTo': b,
                'points': pts
            })
            
    return result


def build_composition_points(problem_data: ProblemData, points: Points) -> Points:
    elementary = [(a, b) for a in problem_data.scheme.variables for b in vbl.post(problem_data.scheme, a)]
    result = defaultdict(dict)
    for a, b in elementary:
        result[a][b] = points[a][b]
        
    queue = elementary
    while queue:
        a, b = queue[0]
        queue = queue[1:]
        for c in vbl.post(problem_data.scheme, b):
            composed = compose_points(result[a][b], result[b][c]) 
            if c in result[a]:
                print(f'{(a, c)} already calculated, skipping')
                continue
            
            result[a][c] = composed
            queue.append((a, c))
            
    return result
            
            
def get_influence_value(f: list[Point], x: float) -> float:
    index_left = bisect.bisect_right(f, x, key=lambda p: p.x) - 1
    index_right = index_left + (index_left < len(f) - 1)
    
    if index_left == index_right:
        return f[index_left].y
    
    x1, y1 = f[index_left].x, f[index_left].y
    x2, y2 = f[index_right].x, f[index_right].y
    
    return ((y2 - y1) / (x2 - x1)) * (x - x1) + y1


def get_influence_x(value: float, x1: float, x2: float, y1: float, y2: float) -> float:
    return x1 + ((value - y1) / (y2 - y1)) * (x2 - x1)
            
            
def compose_points(f: list[Point], g: list[Point]) -> list[Point]:
    result = [] 
    
    x1 = f[0].x
    y1 = f[0].y
    result.append(
        Point(x1, get_influence_value(g, y1))
    ) 
    
    for i in range(1, len(f)):
        x2 = f[i].x
        y2 = f[i].y
        
        intermediate = [p.x for p in g if p.x > y1 and p.x < y2]
        for p in intermediate:
            result.append(
                Point(
                    get_influence_x(p, x1, x2, y1, y2),
                    get_influence_value(g, p)
                )
            )
        
        result.append(
            Point(x2, get_influence_value(g, y2))
        )
        
        x1 = x2
        y1 = y2
            
    return result