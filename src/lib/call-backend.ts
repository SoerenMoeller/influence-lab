import { spawn } from 'child_process';

export async function callHaskell(): Promise<Statement[]> {  
    return new Promise((resolve, reject) => {
        const process = spawn('cabal', ['run']); 

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
                resolve(JSON.parse(output));
            } catch (e) {
                reject(new Response(JSON.stringify({ error: 'Invalid JSON output' }), { status: 500 }));
            }
        });

        process.stdin.end();
    });
}
