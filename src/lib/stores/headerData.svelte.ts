export type HeaderData = {
    normalise: (evt: any) => void;
    solve: (evt: any) => void;
    currentProblem: ProblemData | null;
    problems: ProblemData[];
    solverType: Solver;
}

export let headerData: HeaderData = $state({ 
    normalise: (evt: any) => {},
    solve: (evt: any) => {},
    currentProblem: null,
    problems: [],
    solverType: 'sat'
});
