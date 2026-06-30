import { loadFromStorage, saveToStorage } from '$lib/stores/persistence';
import type { ProblemData } from '$lib/types/problemData';
import type { LongStatement } from '$lib/types/statement';

export type Settings = {
    showHypothesis: boolean;
}

class AppStateStore {
    problemPool = $state<ProblemData[]>([]);
    selectedProblemIndex = $state<number | null>(null);
    isShowingNormalised = $state(false);
    normalisedProblem = $state<ProblemData | null>(null);
    highlightedStatement = $state<LongStatement | null>(null);
    settings = $state<Settings>({ showHypothesis: true });

    get problem(): ProblemData | null {
        return this.selectedProblemIndex !== null
            ? this.problemPool[this.selectedProblemIndex] ?? null
            : null;
    }

    restoreFromStorage() {
        const saved = loadFromStorage();
        this.settings.showHypothesis = saved.showHypothesis ?? true;
        this.isShowingNormalised = saved.isShowingNormalised ?? false;
        this.selectedProblemIndex = saved.selectedProblemIndex ?? 0;
    }

    persist() {
        saveToStorage({
            showHypothesis: this.settings.showHypothesis,
            selectedProblemIndex: this.selectedProblemIndex ?? 0,
            isShowingNormalised: this.isShowingNormalised,
        });
    }
}

export const appState = new AppStateStore();
