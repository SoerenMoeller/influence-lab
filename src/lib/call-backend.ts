import { spawn } from 'child_process';

export type ScriptName = 'scheme' | 'normalise' | 'solver';

export async function callPython(script: string, args?: string): Promise<any> {  
    return new Promise<any>((resolve, reject) => {
        const process = spawn('backend/.venv/bin/python', ["backend/" + script + ".py", ...(args ? [args] : [])]);

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
                console.log('Reject');
                console.log('Error:');
                console.error(error);
                console.log('Output:');
                console.log(output);
                reject(new Response(JSON.stringify({ error }), { status: 500 }));
                return;
            } 
            
            try {
                const marker = '<<<RESULT>>>';
                const markerIndex = output.indexOf(marker);

                if (markerIndex === -1) {
                    throw new Error('Marker string not found in output');
                }

                // Extract everything after the marker line, including possible newline(s)
                const jsonStartIndex = markerIndex + marker.length;
                const jsonString = output.slice(jsonStartIndex).trim();

                // console.log(jsonString)
                resolve(JSON.parse(jsonString));
            } catch (e) {
                reject(new Response(JSON.stringify({ error: 'Invalid JSON output' }), { status: 500 }));
            }
        });

        process.stdin.end();
    });
}