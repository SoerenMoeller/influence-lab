import { callPython } from '$lib/call-backend';
import type { RequestHandler } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
    try {
        const inputScheme: ProblemDataSerialized = await request.json();
        const json = JSON.stringify(inputScheme);
        const result = await callPython('normalise', json);

        return new Response(JSON.stringify(result), {
            headers: { 'Content-Type': 'application/json' }
        });
    } catch (err) {
        console.error("Normalise error:", err);
        return new Response('Error normalising scheme', { status: 500 });
    }
};
