from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float 
    
    
@dataclass 
class Points:
    points: dict[str, dict[str, list[Point]]]
    

def serialise_point(point: Point) -> dict:
    return {
        'x': point.x,
        'y': point.y
    }
    

def deserialise_point(data: dict) -> Point:
    return Point(data['x'], data['y'])


def serialise_points(points: Points) -> list:
    result = []
    for a in points.points:
        for b in points.points[a]:
            pts = [serialise_point(p) for p in points.points[a][b]] 
            result.append({
                'variableFrom': a,
                'variableTo': b,
                'points': pts
            })
            
    return result
