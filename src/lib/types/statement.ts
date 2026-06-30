export type Statement = {
    domain:    Interval;
    behaviour: Behaviour;
    range:     Interval;
}

export type LongStatement = {
    variableFrom: string; 
    domain:       Interval;
    behaviour:    Behaviour;
    range:        Interval;
    variableTo:   string;
}

export function equalLongStatements(a: LongStatement | null, b: LongStatement | null): boolean {
    if (a == null || b == null) {
        return false;
    }
    
    return (
        a.variableFrom === b.variableFrom &&
        a.variableTo === b.variableTo &&
        a.behaviour === b.behaviour &&
        a.domain.start === b.domain.start &&
        a.domain.end === b.domain.end &&
        a.range.start === b.range.start &&
        a.range.end === b.range.end
    );
}
