export function serialiseProblemData(problemData: ProblemData): ProblemDataSerialized {
    return {
        scheme: serialiseScheme(problemData.scheme),
        hypothesis: problemData.hypothesis
    }
}


export function deserialiseProblemData(data: ProblemDataSerialized): ProblemData {
    return {
        scheme: deserializeScheme(data.scheme),
        hypothesis: data.hypothesis
    }
}


export function serialiseScheme(scheme: Scheme): SchemeSerialized {
    const variables = Array.from(scheme.variables);
    const order = Array.from(scheme.order.entries()).map(([variableFrom, variableTos]) => ({
        variableFrom,
        variableTos: Array.from(variableTos),
    }));

    const statements = Array.from(scheme.statements.entries()).flatMap(([variableFrom, variableToStatements]) => 
        Array.from(variableToStatements.entries()).map(([variableTo, statements]) => ({
            variableFrom,
            variableTo,
            statements
        }))
    );

    return {
        variables,
        order,
        statements,
    };
}

export function deserializeScheme(data: SchemeSerialized): Scheme {
    const variables = new Set(data.variables);
    const order = new Map(data.order.map(({ variableFrom, variableTos }) => [variableFrom, new Set(variableTos)]));
    const statements = new Map<string, Map<string, Statement[]>>();

    for (const { variableFrom, variableTo, statements: stmt } of data.statements) {
        if (!statements.has(variableFrom)) {
            statements.set(variableFrom, new Map());
        }
        statements.get(variableFrom)!.set(variableTo, stmt);
    }

    return {
        variables,
        order,
        statements,
    };
}

export function serialisePoints(points: Points): PointsSerialized {
    const serialized: PointsSerialized = [];

    for (const [variableFrom, variableToPoints] of points.entries()) {
        for (const [variableTo, pointArray] of variableToPoints.entries()) {
            serialized.push({
                variableFrom,
                variableTo,
                points: pointArray
            });
        }
    }

    return serialized;    
}

export function deserializePoints(data: PointsSerialized): Points {
    const result: Points = new Map();

    for (const entry of data) {
        if (!result.has(entry.variableFrom)) {
            result.set(entry.variableFrom, new Map());
        }
        result.get(entry.variableFrom)!.set(entry.variableTo, entry.points);
    }
    
    return result;
}