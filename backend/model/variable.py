from model.scheme import Scheme


def post(scheme: Scheme, variable: str) -> set[str]:
    result = set()
    for target in scheme.order[variable]:
        is_transitive = False
        for via in scheme.order[variable]:
            if via != target and target in scheme.order.get(via, set()):
                is_transitive = True
                break
        if not is_transitive:
            result.add(target)
    return result


def pre(scheme: Scheme, variable: str) -> set[str]:
    return {var for var in scheme.variables if variable in post(scheme, var)}


def is_maximal(variable: str, scheme: Scheme) -> bool:
    for var in post(scheme, variable):
        if post(scheme, var):
            return False
    return True


def is_minimal(scheme: Scheme, variable: str) -> bool:
    return not pre(scheme, variable)