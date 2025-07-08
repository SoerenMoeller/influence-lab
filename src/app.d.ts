// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
	namespace App {
	}

    type Interval = {
        start: Double;
        end:   Double;
    }

    type Behaviour = MONO | ANTI | CONST | ARB;
    
    type LongStatement = {
        variableFrom: string;
        domain:       Interval;
        behaviour:    Behaviour;
        range:        Interval;
        variableTo:   string;
    }

    type StatementList = LongStatement[];

    type Statement = {
        domain:    Interval;
        behaviour: Behaviour;
        range:     Interval;
    }

    type Scheme = Map<string, Map<string, Statement[]>>;
    
    type Points = Map<string, Map<string, {x: number, y: number}[]>>
}

export {};
