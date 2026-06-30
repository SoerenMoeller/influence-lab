import * as problemData from "$lib/types/problemData";
import { PUBLIC_API_URL } from '$env/static/public';

type LoadResult = {
    problems: ProblemData[];
};

export const load = async ({ fetch }): Promise<LoadResult> => {
    const res = await fetch(`${PUBLIC_API_URL}/api/schemes`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    });

    if (!res.ok) {
        const text = await res.text();
        console.error("Failed to load:", text);
        throw new Error(text);
    }

    const data = await res.json();
    const problems = data.map((d: any) => problemData.deserialiseProblemData(d));
    return {
        problems: problems
    };
};

export const prerender = true;

