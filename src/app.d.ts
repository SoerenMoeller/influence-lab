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
    
    type Statement = {
        variableFrom: string;
        domain:       Interval;
        behaviour:    Behaviour;
        range:        Interval;
        variableTo:   string;
    }
}

export {};
