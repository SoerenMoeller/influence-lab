import sys

from model.scheme import Scheme
import src.io as io
import src.normalise as normalise


def main() -> int:
    args = sys.argv[1]
    statements = io.json_to_statement_list(args)
    scheme = Scheme(statements)
    scheme = normalise.normalise(scheme)
    result = io.statement_list_to_json(
        io.scheme_to_statement_list(scheme)
    )
    print(result)

    return 0


if __name__ == '__main__':
    main()