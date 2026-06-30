type VariableMap<T> = Map<string, Map<string, T>>;

export type Scheme = {
    statements: VariableMap<Statement[]>;
    variables:  Set<string>;
    order:      Map<string, Set<string>>; 
}

export type SchemeSerialised = {
    variables: string[];
    order: {
        variableFrom: string;
        variableTos:  string[];
    }[];
    statements: {
        variableFrom: string;
        variableTo:   string;
        statements:   Statement[];
    }[];
};

export function serialiseScheme(scheme: Scheme): SchemeSerialised {
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

export function deserialiseScheme(data: SchemeSerialised): Scheme {
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
