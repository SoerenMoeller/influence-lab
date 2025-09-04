/*
    * test
*/
export function initialiseDefaultPoints(problemData: ProblemData) {
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
