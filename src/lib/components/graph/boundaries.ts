/*
* This function calculates the boundaries (min and max values) for a given variable based on the
* provided scheme and hypothesis. It adds padding to the boundaries to ensure that the range is not
* too tight.
*/
export function getBoundaries(
    variable: string, 
    scheme: Scheme, 
    hypothesis: LongStatement | null
): { min: number; max: number } {
    const variablesTo = scheme.order.get(variable) ?? [];
    const variablesFrom = [...scheme.variables].filter((v: string) =>
        scheme.order.get(v)?.has(variable),
    );

    const values = collectValues(variablesTo, variablesFrom, variable, scheme, hypothesis);

    if (values.size === 0) {
        return { min: -1, max: 1 };
    }

    const rawMin = Math.min(...values);
    const rawMax = Math.max(...values);
    
    const span = rawMax - rawMin;
    const offset = span === 0 ? 1 : span * 0.1;

    return {
        min: rawMin - offset,
        max: rawMax + offset,
    };
}

function collectValues(variablesTo: Set<string>, variablesFrom: Set<string>, variable: string, scheme: Scheme, hypothesis: LongStatement | null): Set<number> {
    const values = new Set<number>();

    for (const v of variablesTo) {
        const statements = scheme.statements.get(variable)?.get(v);
        if (!statements) continue;

        if (hypothesis?.variableFrom == variable && hypothesis?.variableTo == v) {
            values.add(hypothesis.domain.start);
            values.add(hypothesis.domain.end);
        }

        for (const st of statements) {
            values.add(st.domain.start);
            values.add(st.domain.end);
        }
    }

    for (const v of variablesFrom) {
        const statements = scheme.statements.get(v)?.get(variable);
        if (!statements) continue;

        if (hypothesis?.variableFrom == v && hypothesis?.variableTo == variable) {
            values.add(hypothesis.range.start);
            values.add(hypothesis.range.end);
        }

        for (const st of statements) {
            values.add(st.range.start);
            values.add(st.range.end);
        }
    }

    return values;
}
