<script lang="ts">
    import * as d3 from "d3";
    import StatementComponent from "./Statement.svelte";
    import SVG from "./SVG.svelte";
    import { svgConfig } from "$lib/modules/svgConfig";

    const props = $props();
    const scheme: Scheme = $derived(props.scheme) as Scheme;
    const variableFrom: string = props.variableFrom as string;
    const variableTo: string = props.variableTo as string;
    const hypothesis: Hypothesis = props.hypothesis;
    const points: Point[] = $derived(props.points);
    const statements = $derived(
        scheme.statements.get(variableFrom)?.get(variableTo) ?? [],
    );

    const boundsVariableFrom = $derived(getBoundaries(variableFrom));
    const boundsVariableTo = $derived(getBoundaries(variableTo));
    const offsetVariableFrom = $derived.by(() => {
        if ((boundsVariableFrom.max - boundsVariableFrom.min) == 0) {
            return 1;
        } else {
            return (boundsVariableFrom.max - boundsVariableFrom.min) * 0.1;
        }
    });
    const offsetVariableTo = $derived.by(() => {
        if ((boundsVariableTo.max - boundsVariableTo.min) == 0) {
            return 1;
        } else {
            return (boundsVariableTo.max - boundsVariableTo.min) * 0.1;
        }
    });

    const minValueDomain = $derived(
        boundsVariableFrom.min - offsetVariableFrom,
    );
    const maxValueDomain = $derived(
        boundsVariableFrom.max + offsetVariableFrom,
    );
    const minValueRange = $derived(boundsVariableTo.min - offsetVariableTo);
    const maxValueRange = $derived(boundsVariableTo.max + offsetVariableTo);

    const xMapping = $derived(
        d3
            .scaleLinear()
            .domain([minValueDomain, maxValueDomain])
            .range([
                svgConfig.marginLeft,
                svgConfig.width - svgConfig.marginRight,
            ]),
    );
    const yMapping = $derived(
        d3
            .scaleLinear()
            .domain([minValueRange, maxValueRange])
            .range([
                svgConfig.height - svgConfig.marginBottom,
                svgConfig.marginTop,
            ]),
    );

    function getBoundaries(variable: string): { min: number; max: number } {
        const variablesTo = scheme.order.get(variable) ?? [];
        const variablesFrom = [...scheme.variables].filter((v: string) =>
            scheme.order.get(v)?.has(variable),
        );

        const values = new Set<number>();

        for (const v of variablesTo) {
            const statements = scheme.statements.get(variable)?.get(v);
            if (!statements) continue;

            if (
                hypothesis.variableFrom == variable &&
                hypothesis.variableTo == v
            ) {
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

            if (
                hypothesis.variableFrom == v &&
                hypothesis.variableTo == variable
            ) {
                values.add(hypothesis.range.start);
                values.add(hypothesis.range.end);
            }

            for (const st of statements) {
                values.add(st.range.start);
                values.add(st.range.end);
            }
        }

        return {
            min: Math.min(...values),
            max: Math.max(...values),
        };
    }
</script>

<SVG
    {minValueDomain}
    {maxValueDomain}
    {minValueRange}
    {maxValueRange}
    {xMapping}
    {yMapping}
    xLabel={variableFrom}
    yLabel={variableTo}
>
    {#each statements as st}
        <StatementComponent
            statement={st}
            {xMapping}
            {yMapping}
            highlighted={false}
        />
    {/each}

    {#if variableFrom == hypothesis.variableFrom && variableTo == hypothesis.variableTo}
        <StatementComponent
            statement={{
                domain: hypothesis.domain,
                behaviour: hypothesis.behaviour,
                range: hypothesis.range,
            }}
            highlighted={true}
            {xMapping}
            {yMapping}
        />
    {/if}

    {#each points as point}
        <circle
            r="5"
            cx={xMapping(point.x)}
            cy={yMapping(point.y)}
            fill="red"
        />
    {/each}

    {#if points && points.length > 1}
        {#each Array(points.length - 1) as _, idx}
            <line
                x1={xMapping(points[idx].x)}
                y1={yMapping(points[idx].y)}
                x2={xMapping(points[idx + 1].x)}
                y2={yMapping(points[idx + 1].y)}
                style="stroke:red;stroke-width:2"
            />
        {/each}
    {/if}
</SVG>
