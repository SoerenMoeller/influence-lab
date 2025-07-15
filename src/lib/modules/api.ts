import { PUBLIC_API_URL } from '$env/static/public';
import * as transform from "$lib/modules/transform";
import * as pts from "$lib/modules/points";
import { removeNotification, showNotification } from '$lib/stores/notification.svelte';


export async function normalise(problemData: ProblemData): Promise<ProblemData> {
    const serialised = transform.serialiseProblemData(problemData);
    const notification = showNotification('Normalising Scheme...', 'delay')
    const res = await fetch(`${PUBLIC_API_URL}/api/normalise`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(serialised)
    });
    removeNotification(notification);

    if (!res.ok) {
        console.error("Failed to normalise:", await res.text());
        showNotification("Scheme could not be normalised.", "error");
        return problemData;
    }

    const normalisedSerialised = await res.json();
    const normalisedProblem = transform.deserialiseProblemData(normalisedSerialised);
 
    showNotification("Scheme successfully normalised.", "success");
    return normalisedProblem;
}


export async function solve(problemData: ProblemData, solverType: Solver): Promise<Points> {
    const serialised = transform.serialiseProblemData(problemData);
    const data = {
        problem: serialised,
        solver: solverType
    }

    const notification = showNotification('Solving Scheme using "' + solverType + '" stategy', 'delay')
    const res = await fetch(`${PUBLIC_API_URL}/api/solve`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    removeNotification(notification);

    if (!res.ok) {
        console.error("Failed to solve:", await res.text());
        showNotification("Scheme could not be solved.", "error");
        return pts.initialiseDefaultPoints(problemData);
    }

    const result = await res.json();
    if (result.result) {
        const points = transform.deserializePoints(result.points);
        showNotification("Scheme successfully solved.", "success");
        return points;
    }
    
    showNotification("Scheme is unsolvable.", "error");
    return pts.initialiseDefaultPoints(problemData);
}

    