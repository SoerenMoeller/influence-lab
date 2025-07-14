import { PUBLIC_API_URL } from '$env/static/public';
import * as transform from "$lib/modules/transform";
import * as pts from "$lib/modules/points";
import { showNotification } from '$lib/stores/notification';


export async function normalise(problemData: ProblemData): Promise<ProblemData> {
    const serialised = transform.serialiseProblemData(problemData);
    const res = await fetch(`${PUBLIC_API_URL}/api/normalise`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(serialised)
    });

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


export async function solve(problemData: ProblemData): Promise<Points> {
    const serialised = transform.serialiseProblemData(problemData);
    const res = await fetch(`${PUBLIC_API_URL}/api/solve`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(serialised)
    });

    if (!res.ok) {
        console.error("Failed to normalise:", await res.text());
        showNotification("Scheme could not be normalised.", "error");
        return pts.initialiseDefaultPoints(problemData);
    }

    const pointsSerialised = await res.json();
    const points = transform.deserializePoints(pointsSerialised);
 
    showNotification("Scheme successfully solved.", "success");
    return points;
}

    