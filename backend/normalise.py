import sys

from model.scheme import Scheme
import src.io as io
import src.normalise as normalise


def main() -> int:
    args = sys.argv[1]
    problem_data = io.deserialise_problem_data(args)
    problem_data = normalise.normalise(problem_data)
    result = io.serialise_problem_data(problem_data)
    print('<<<RESULT>>>')
    print(result)

    return 0


if __name__ == '__main__':
    main()