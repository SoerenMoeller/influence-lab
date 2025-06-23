import { spawn } from 'child_process';

export type ScriptName = 'get-scheme' | 'normalise';

export async function callHaskell(script: ScriptName, args?: string): Promise<StatementList> {  
    return new Promise((resolve, reject) => {
        const process = spawn('cabal', ['exec', '--', script, ...(args ? [args] : [])]);

        let output: string = '';
        let error: string = '';

        process.stdout.on('data', (data: string) => {
            output += data;
        });

        process.stderr.on('data', (data: string) => {
            error += data.toString();
        });

        process.on('close', (code: number) => {
            if (code !== 0) {
                reject(new Response(JSON.stringify({ error }), { status: 500 }));
                return;
            } 
            
            try {
                const scheme: StatementList = JSON.parse(JSON.parse(output)) as StatementList;
                resolve(scheme);
            } catch (e) {
                reject(new Response(JSON.stringify({ error: 'Invalid JSON output' }), { status: 500 }));
            }
        });

        process.stdin.end();
    });
}
