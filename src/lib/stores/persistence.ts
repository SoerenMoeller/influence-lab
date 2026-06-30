const STORAGE_KEY = 'influence-lab-app-data';

export type PersistedState = {
    showHypothesis: boolean;
    selectedProblemIndex: number;
    isShowingNormalised: boolean;
}

export function loadFromStorage(): Partial<PersistedState> {
    if (typeof localStorage === 'undefined') return {};
    try {
        const raw = localStorage.getItem(STORAGE_KEY);
        return raw ? JSON.parse(raw) : {};
    } catch { return {}; }
}

export function saveToStorage(state: PersistedState): void {
    if (typeof localStorage === 'undefined') return;
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch {}
}
