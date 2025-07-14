export let normaliseButtonAction: {action: (evt: any) => void} = $state({
    action: (evt: any) => {}
});

export let solveButtonAction: {action: (evt: any) => void} = $state({
    action: (evt: any) => {}
});

export function setNormaliseAction(fn: ((evt: any) => void)) {
    normaliseButtonAction.action = fn;
}

export function setSolveAction(fn: ((evt: any) => void)) {
    solveButtonAction.action = fn;
}