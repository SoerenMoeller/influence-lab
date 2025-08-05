<script lang="ts">
    import * as d3 from "d3";
    import StatementComponent from "./Statement.svelte";
    import SVG from "./SVG.svelte";
    import { svgConfig } from "$lib/modules/svgConfig";

    const props = $props();
    const scheme: Scheme         = $derived(props.scheme) as Scheme;
    const variableFrom: string   = props.variableFrom as string;
    const variableTo: string     = props.variableTo as string;
    const hypothesis: Hypothesis = props.hypothesis;
    const points: Point[]        = $derived(props.points);
    const statements             = $derived(scheme.statements.get(variableFrom)?.get(variableTo) ?? []);

    const minValueDomain = $derived(getBoundaries(variableTo).min - 1);
    const maxValueDomain = $derived(getBoundaries(variableTo).max + 1);
    const minValueRange  = $derived(getBoundaries(variableFrom).min - 1);
    const maxValueRange  = $derived(getBoundaries(variableFrom).max + 1);
    
    const xMapping = $derived(
        d3.scaleLinear()
            .domain([minValueDomain - 1, maxValueDomain + 1])
            .range([svgConfig.marginLeft, svgConfig.width - svgConfig.marginRight])
    );
    const yMapping = $derived(
        d3.scaleLinear()
            .domain([minValueRange - 1, maxValueRange + 1])
            .range([svgConfig.height - svgConfig.marginBottom, svgConfig.marginTop])
    );

    function getBoundaries(variable: string): { min: number, max: number } {
        const variablesTo = scheme.order.get(variable) ?? [];
        const variablesFrom = [...scheme.variables].filter((v: string) => scheme.order.get(v)?.has(variable));

        const values = new Set<number>();
        
        for (const v of variablesTo) {
            const statements = scheme.statements.get(variable)?.get(v);
            if (!statements) continue; 

            if (hypothesis.variableFrom == variable && hypothesis.variableTo == v) {
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

            if (hypothesis.variableFrom == v && hypothesis.variableTo == variable) {
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
            max: Math.max(...values)
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
    xLabel = {variableFrom}
    yLabel = {variableTo}
>
    {#each statements as st}
        <StatementComponent statement={st} {xMapping} {yMapping} highlighted={false} />        
    {/each}
    
    {#if variableFrom == hypothesis.variableFrom && variableTo == hypothesis.variableTo}
        <StatementComponent 
            statement={
                {domain: hypothesis.domain, behaviour: hypothesis.behaviour, range: hypothesis.range}
            } 
            highlighted={true}
            {xMapping} {yMapping} 
        />
    {/if}
    
    {#each points as point}
        <circle r="5" cx={xMapping(point.x)} cy={yMapping(point.y)} fill="red" />                         
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
