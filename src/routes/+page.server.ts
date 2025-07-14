import { callPython } from "$lib/call-backend"; 
import * as transform from "$lib/modules/transform";

type LoadResult = {
    result: ProblemData;
};

export const load = async (args): Promise<LoadResult> => {
    const result: ProblemDataSerialized = await callPython('scheme'); 
    const problemData: ProblemData = transform.deserialiseProblemData(result);
    return {
        result: problemData
    };
};

