from dataclasses import dataclass


Boundaries = dict[str, list[float]]
PoiSizes = dict[str, dict[tuple[float, float], int]]
TPSizes = dict[str, dict[tuple[float, float], int]]
Sizes = dict[str, int]
OriginalPoints = dict[str, dict[float, int]]


@dataclass
class PointsCache:
    boundaries: Boundaries
    poi_sizes: PoiSizes
    tp_sizes: TPSizes
    sizes: Sizes
    og_points: OriginalPoints
