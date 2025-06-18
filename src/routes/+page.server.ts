import { callHaskell } from "$lib/call-backend"; 

export const load = async (args) => {
    const result: Statement[] = await callHaskell(); 
    return {
        result
    };
};

