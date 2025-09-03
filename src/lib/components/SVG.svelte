<script lang="ts">
    import * as d3 from "d3";
    import { onMount } from "svelte";
    import { svgConfig } from "$lib/modules/svgConfig";

    let container: HTMLDivElement;
    const { children, ...props } = $props();
    const xLabel = props.xLabel;
    const yLabel = props.yLabel;
    const xMapping = props.xMapping;
    const yMapping = props.yMapping;
    let isHovered = $state(false);
    let mouseCoords = $state({ x: 0, y: 0 });

    let xAxis: SVGGElement;
    let yAxis: SVGGElement;

    onMount(() => {
        d3.select(xAxis)
            .call(d3.axisBottom(xMapping))
            .selectAll(".tick text")
            .attr("class", "text-base");

        d3.select(yAxis)
            .call(d3.axisLeft(yMapping))
            .selectAll(".tick text")
            .attr("class", "text-base");
    });
</script>

<div
    bind:this={container}
    class="w-full bg-white rounded-xl shadow p-6 relative"
>
    <svg
        class="w-full h-auto block cursor-default focus:outline-none"
        viewBox={`0 0 ${svgConfig.width} ${svgConfig.height}`}
        preserveAspectRatio="xMidYMin meet"
        role="button"
        tabindex="0"
        onmouseover={() => (isHovered = true)}
        onmouseout={() => (isHovered = false)}
        onfocus={() => {}}
        onblur={() => {}}
        onmousemove={(evt) => {
            const svg = evt.currentTarget as SVGSVGElement;
            const pt = svg.createSVGPoint();
            pt.x = evt.clientX;
            pt.y = evt.clientY;
            const svgP = pt.matrixTransform(svg.getScreenCTM()?.inverse());

            mouseCoords = {
                x: xMapping.invert(svgP.x),
                y: yMapping.invert(svgP.y),
            };
        }}
    >
        <g
            transform={`translate(0,${svgConfig.height - svgConfig.marginBottom})`}
            bind:this={xAxis}
        />
        <g
            transform={`translate(${svgConfig.marginLeft},0)`}
            bind:this={yAxis}
        />

        <text
            x={svgConfig.width / 2}
            y={svgConfig.height - svgConfig.marginBottom / 4}
            fill="black"
            class="text-2xl"
        >
            {xLabel}
        </text>

        <text
            x={svgConfig.marginLeft}
            y={svgConfig.height / 2 - svgConfig.marginLeft / 4}
            fill="black"
            class="text-2xl"
            text-anchor="middle"
            transform={`rotate(-90, ${svgConfig.marginLeft / 2}, ${svgConfig.height / 2})`}
        >
            {yLabel}
        </text>

        {@render children()}
    </svg>

    {#if isHovered}
        <div
            class="absolute bottom-4 left-4 bg-gray-200 text-gray-900 p-2 rounded
                shadow text-base"
        >
            x: {mouseCoords.x.toFixed(2)}, y: {mouseCoords.y.toFixed(2)}
        </div>
    {/if}
</div>
