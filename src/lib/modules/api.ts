import { PUBLIC_API_URL } from '$env/static/public';
import { removeNotification, showNotification } from '$lib/stores/notification.svelte';
import { deserialiseProblemData, serialiseProblemData } from '$lib/types/problemData';


export async function normalise(problemData: ProblemData): Promise<ProblemData> {
    const serialised = serialiseProblemData(problemData);
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
    const normalisedProblem = deserialiseProblemData(normalisedSerialised);
 
    showNotification("Scheme successfully normalised.", "success");
    return normalisedProblem;
}
    
