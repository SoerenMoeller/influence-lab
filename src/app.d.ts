// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
	namespace App {
	}
    
    type Solver = 'sat' | 'uninterpreted'

    type Interval = {
        start: Double;
        end:   Double;
    }

    type Behaviour = MONO | ANTI | CONST | ARB;
    
    type Statement = {
        domain:    Interval;
        behaviour: Behaviour;
        range:     Interval;
    }
    
    type Hypothesis = {
        variableFrom: string; 
        domain:       Interval;
        behaviour:    Behaviour;
        range:        Interval;
        variableTo:   string;
    }
    
    type VariableMap<T> = Map<string, Map<string, T>>;

    type Scheme = {
        statements: VariableMap<Statement[]>;
        variables:  Set<string>;
        order:      Map<string, Set<string>>; 
    }
    
    type Point = {
        x: number;
        y: number;
    }

    type Points = VariableMap<Point[]>;
    
    type SchemeSerialised = {
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
    
    type PointsSerialised = {
        variableFrom: string;
        variableTo:   string;
        points:       Point[];
    }[];
    
    type ProblemData = {
        scheme: Scheme;
        hypothesis: Hypothesis;
    }
    
    type ProblemDataSerialsed = {
        scheme: SchemeSerialised;
        hypothesis: Hypothesis;
    }
}

export {};
