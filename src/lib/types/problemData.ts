import { serialiseScheme, deserialiseScheme } from "$lib/types/scheme";
import type { Scheme, SchemeSerialised } from "$lib/types/scheme";

export type ProblemData = {
    schemeVersions: Scheme[];
    hypothesis: LongStatement | null;
}

export type ProblemDataSerialsed = {
    schemeVersions: SchemeSerialised[];
    hypothesis: LongStatement | null;
}

export function serialiseProblemData(problemData: ProblemData): ProblemDataSerialsed {
    return {
        schemeVersions: problemData.schemeVersions.map(s => serialiseScheme(s)),
        hypothesis: problemData.hypothesis != null ? problemData.hypothesis : null
    }
}

export function deserialiseProblemData(data: ProblemDataSerialsed): ProblemData {
    return {
        schemeVersions: data.schemeVersions.map(s => deserialiseScheme(s)),
        hypothesis: data.hypothesis != null ? data.hypothesis : null
    }
}

