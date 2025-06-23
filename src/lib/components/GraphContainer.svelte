<script lang="ts">
    import * as d3 from "d3";
    import StatementComponent from "./Statement.svelte";
    import { showNotification } from "$lib/stores/notification";

    let container: HTMLDivElement;
    const props = $props();
    const scheme: Statement[]  = props.scheme as Statement[];
    const variableFrom: string = props.variableFrom as string;
    const variableTo: string   = props.variableTo as string;

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

    $effect(() => {
        if (xAxis) {
            d3.select(xAxis)
                .call(d3.axisBottom(x))
                .selectAll(".tick text")
                .attr("class", "text-base");
        }
        if (yAxis) {
            d3.select(yAxis)
                .call(d3.axisLeft(y))
                .selectAll(".tick text")
                .attr("class", "text-base");
        }
    });
</script>

<div 
    bind:this={container}
    class="w-full bg-white rounded-xl shadow p-6"
>
    <svg
        class="w-full h-auto block"
        viewBox={`0 0 ${width} ${height}`}
        preserveAspectRatio="xMidYMin meet"
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
</div>

