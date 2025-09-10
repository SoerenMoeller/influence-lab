def test():
    ...


def main():
    import pyperf
    from collections import namedtuple
    import data.flat as flat


    Benchmark = namedtuple('Benchmark', ['name', 'func', 'args'])

    BENCHMARKS = [
        Benchmark(
            name="Flat Scheme",
            func=lambda x, y: flat.get_problem(x, y),
            args=[(1,2), (10,2)]
        ),
    ]
    
    runner = pyperf.Runner()
    
    for bm in BENCHMARKS:
        for args in bm.args:
            runner.bench_func(f"{bm.name}-{args}", lambda f= bm.func, a=args: f(*a))


if __name__ == "__main__":
    main()
    
