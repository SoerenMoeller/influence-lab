from model.scheme import Scheme


def post(variable: str, scheme: Scheme) -> set[str]:
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


def pre(variable: str, scheme: Scheme) -> set[str]:
    return {var for var in scheme.variables if variable in post(var, scheme)}
