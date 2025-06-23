export function statementListToScheme(statementList: StatementList): Scheme {
    const scheme: Scheme = new Map();

    for (const statement of statementList) {
        const { variableFrom, variableTo, domain, behaviour, range } = statement;

        if (!scheme.has(variableFrom)) {
            scheme.set(variableFrom, new Map());
        }

        const toMap = scheme.get(variableFrom)!;

        if (!toMap.has(variableTo)) {
            toMap.set(variableTo, []);
        }

        toMap.get(variableTo)!.push({
            domain,
            behaviour,
            range
        });
    }

    return scheme;
}

export function schemeToStatementList(scheme: Scheme): StatementList {
    const statementList: StatementList = [];

    for (const [variableFrom, toMap] of scheme.entries()) {
        for (const [variableTo, statements] of toMap.entries()) {
            for (const { domain, behaviour, range } of statements) {
                statementList.push({
                    variableFrom,
                    variableTo,
                    domain,
                    behaviour,
                    range
                });
            }
        }
    }

    return statementList;
}
