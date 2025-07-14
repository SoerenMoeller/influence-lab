import * as transform from "$lib/modules/transform";
import { PUBLIC_API_URL } from '$env/static/public';

type LoadResult = {
    result: ProblemData[];
};

export const load = async (args): Promise<LoadResult> => {
        const res = await fetch(`${PUBLIC_API_URL}/api/schemes`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        });

        if (!res.ok) {
            console.error("Failed to load:", await res.text());
        }

        const data = await res.json();
        const problems = data.map((d: any) => transform.deserialiseProblemData(d));
        return {
            result: problems 
        } 
};

