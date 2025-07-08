import { callPython } from '$lib/call-backend';
import type { RequestHandler } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
    try {
        const inputScheme: StatementList = await request.json();
        const json = JSON.stringify(inputScheme);
        const result = await callPython('solver', json);

        return new Response(JSON.stringify(result), {
            headers: { 'Content-Type': 'application/json' }
        });
    } catch (err) {
        console.error("Solver error:", err);
        return new Response('Error solving scheme', { status: 500 });
    }
};
