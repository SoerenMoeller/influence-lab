<script lang="ts">
    import * as d3 from "d3";
    import StatementComponent from "./Statement.svelte";
    import { onMount } from "svelte";

    let container: HTMLDivElement;
    const props = $props();
    const scheme: Statement[]  = props.scheme as Statement[];
    const variableFrom: string = props.variableFrom as string;
    const variableTo: string   = props.variableTo as string;
    const points: {x: number, y: number}[] | undefined = $derived(props.points);
    
    $effect(() => {
        console.log(points);
    })

    let isHovered: boolean = $state(false);

    const width = 1080;
    const height = 720;
    const marginTop = 10;
    const marginRight = 20;
    const marginBottom = 80;
    const marginLeft   = 80;

    const minValueDomain = Math.min(...scheme.map((st: Statement) => st.domain.start));
    const maxValueDomain = Math.max(...scheme.map((st: Statement) => st.domain.end));
    const minValueRange  = Math.min(...scheme.map((st: Statement) => st.range.start));
    const maxValueRange  = Math.max(...scheme.map((st: Statement) => st.range.end));

    const x = d3.scaleLinear()
        .domain([minValueDomain - 1, maxValueDomain + 1])
        .range([marginLeft, width - marginRight]);

    const y = d3.scaleLinear()
        .domain([minValueRange - 1, maxValueRange + 1])
        .range([height - marginBottom, marginTop]);

    let xAxis: SVGGElement; 
    let yAxis: SVGGElement; 
    let mouseCoords = $state({ x: 0, y: 0 });

    onMount(() => {
        d3.select(xAxis)
            .call(d3.axisBottom(x))
            .selectAll(".tick text")
            .attr("class", "text-base");

        d3.select(yAxis)
            .call(d3.axisLeft(y))
            .selectAll(".tick text")
            .attr("class", "text-base");
    });
</script>

<div 
    bind:this={container}
    class="w-full bg-white rounded-xl shadow p-6 relative"
>
    <svg
        class="w-full h-auto block cursor-default"
        viewBox={`0 0 ${width} ${height}`}
        preserveAspectRatio="xMidYMin meet"
        role="button"
        tabindex="0"
        onmouseover={() => isHovered = true}
        onmouseout={() => isHovered = false}
        onfocus={() => {}}
        onblur={() => {}}
        onmousemove={(evt) => {
            const svg = evt.currentTarget as SVGSVGElement;
            const pt = svg.createSVGPoint();
            pt.x = evt.clientX;
            pt.y = evt.clientY;
            const svgP = pt.matrixTransform(svg.getScreenCTM()?.inverse());

            mouseCoords = { 
                x: x.invert(svgP.x),
                y: y.invert(svgP.y)
            };
        }}
    >
        <g 
            transform={`translate(0,${height - marginBottom})`}
            bind:this={xAxis} 
        />

        <g 
            transform={`translate(${marginLeft},0)`}
            bind:this={yAxis} 
        />

        <text
            x={marginLeft}
            y={height / 2 - marginLeft / 4}
            fill="black"
            class="text-2xl"
            text-anchor="middle"
            transform={`rotate(-90, ${marginLeft / 2}, ${height / 2})`}
        >
            {variableTo}
        </text>

        <text
            x={width / 2}
            y={height - marginBottom / 4}
            fill="black"
            class="text-2xl"
        >
            {variableFrom}
        </text>

        {#each scheme as st}
            <StatementComponent statement={st} {x} {y} />        
        {/each}
    </svg>

    
    {#if isHovered}
        <div 
            class="absolute bottom-4 left-4 bg-gray-200 text-gray-900 p-2 rounded 
                shadow text-base">
            x: {mouseCoords.x.toFixed(2)}, y: {mouseCoords.y.toFixed(2)}
        </div>
    {/if}
</div>

