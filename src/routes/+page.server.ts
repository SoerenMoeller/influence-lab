import { callHaskell } from "$lib/call-backend"; 
import * as io from "$lib/modules/scheme/io";

type LoadResult = {
    result: Scheme;
};

export const load = async (args): Promise<LoadResult> => {
    const result: StatementList = await callHaskell('get-scheme'); 
    const scheme: Scheme = io.statementListToScheme(result); 
    return {
        result: scheme
    };
};

