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

    const minValueDomain = $derived(Math.min(...statements.map((st: Statement) => st.domain.start)));
    const maxValueDomain = $derived(Math.max(...statements.map((st: Statement) => st.domain.end)));
    const minValueRange  = $derived(Math.min(...statements.map((st: Statement) => st.range.start)));
    const maxValueRange  = $derived(Math.max(...statements.map((st: Statement) => st.range.end)));
    
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
