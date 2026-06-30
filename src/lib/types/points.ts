type VariableMap<T> = Map<string, Map<string, T>>;

type Point = {
    x: number;
    y: number;
}

type Points = VariableMap<Point[]>;

export function serialisePoints(points: Points): PointsSerialised {
    const serialized: PointsSerialised = [];

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

export function deserialisePoints(data: PointsSerialised): Points {
    const result: Points = new Map();

    for (const entry of data) {
        if (!result.has(entry.variableFrom)) {
            result.set(entry.variableFrom, new Map());
        }
        result.get(entry.variableFrom)!.set(entry.variableTo, entry.points);
    }
    
    return result;
}

export function getBoundaryPoints(problemData: ProblemData) {
    const initialPoints: Points = new Map();

    for (const [from, toSet] of problemData.scheme.order) {
        if (!initialPoints.has(from)) {
            initialPoints.set(from, new Map());
        }

        const innerMap = initialPoints.get(from)!;
        for (const to of toSet) {
            innerMap.set(to, []); 
        }
    }
    
    return initialPoints;
}
