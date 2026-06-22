export type HeaderData = {
    normalise: (evt: any) => void;
    solve: (evt: any) => void;
    currentProblem: ProblemData | null;
    problems: ProblemData[];
    solverType: Solver;
    showHypothesis: boolean;
}

const STORAGE_KEY = 'influence-lab-header';

function loadFromStorage() {
    try {
        const raw = localStorage.getItem(STORAGE_KEY);
        return raw ? JSON.parse(raw) : {};
    } catch { return {}; }
}

function saveToStorage() {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({
            showHypothesis: headerData.showHypothesis,
            currentProblemIndex: headerData.problems.indexOf(headerData.currentProblem),
        }));
    } catch {}
}

const saved = loadFromStorage();

export let headerData: HeaderData = $state({
    normalise: (evt: any) => {},
    solve: (evt: any) => {},
    currentProblem: null,
    problems: [],
    solverType: 'incremental',
    showHypothesis: saved.showHypothesis ?? true,
});

export function restoreFromStorage() {
    const idx = saved.currentProblemIndex ?? 0; // your original default
    headerData.currentProblem = headerData.problems[idx] ?? headerData.problems[0];
}

export { saveToStorage };
