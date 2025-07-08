import sys


import src.io as io
import src.points as points
import model.variable as vbl
from model.scheme import Scheme
from scheme import schemes


def main() -> int:
    # args = sys.argv[1]
    # statements = io.json_to_statement_list(args)
    # scheme = Scheme(statements)
    scheme = schemes[0]
    for v in ['d', 'c', 'b', 'a']:
        ps = points.boundaries(scheme, v)
        for i in range(len(ps) - 1):
            distance = points.dist_tp(scheme, v, ps[i], ps[i + 1])
            print(f'dist_tp({v}, {ps[i]}, {ps[i + 1]}) = {distance}')
    print('---------------')
    for v1 in ['d', 'c', 'b', 'a']:
        for v2 in vbl.post(scheme, v1):
            ps = points.boundaries(scheme, v1)
            for i in range(len(ps) - 1):
                distance = points.dist_tp2(scheme, v1, v2, ps[i], ps[i + 1])
                print(f'dist_tp2({v1}, {v2}, {ps[i]}, {ps[i + 1]}) = {distance}')
    print('===============')
    for v in ['a', 'b', 'c', 'd']:
        ps = points.boundaries(scheme, v)
        for i in range(len(ps) - 1):
            distance = points.dist_poi(scheme, v, ps[i], ps[i + 1])
            print(f'dist_poi2({v}, {ps[i]}, {ps[i + 1]}) = {distance}')
    print('---------------')
    for v1 in ['a','b', 'c', 'd']:
        for v2 in vbl.pre(scheme, v1):
            ps = points.boundaries(scheme, v2)
            for i in range(len(ps) - 1):
                distance = points.dist_poi2(scheme, v2, v1, ps[i], ps[i + 1])
                print(f'dist_poi2({v1}, {v2}, {ps[i]}, {ps[i + 1]}) = {distance}')
    print('===============')
    for v in ['a','b', 'c', 'd']:
        for p in points.boundaries(scheme, v):
            point = points.get_original_point(scheme, v, p)
            print(f'get_original_point({v}, {p}) = {point}')
    return 0


if __name__ == '__main__':
    main()
