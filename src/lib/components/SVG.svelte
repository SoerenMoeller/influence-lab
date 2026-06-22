<script lang="ts">
    import * as d3 from "d3";
    import { onMount } from "svelte";
    import { svgConfig } from "$lib/modules/svgConfig";

    let container: HTMLDivElement;
    let { children, xLabel, yLabel, xMapping, yMapping } = $props();
    let isHovered = $state(false);
    let mouseCoords = $state({ x: 0, y: 0 });
    let xAxis: SVGGElement;
    let yAxis: SVGGElement;

    onMount(() => {
        d3.select(xAxis)
            .call(d3.axisBottom(xMapping).ticks(5))
            .call((g) => g.select(".domain").attr("stroke", "#d1d5db"))
            .call((g) => g.selectAll(".tick line").attr("stroke", "#e5e7eb"))
            .call((g) =>
                g
                    .selectAll(".tick text")
                    .attr("fill", "#6b7280")
                    .attr("font-size", "11px")
                    .attr("font-family", "inherit"),
            );

        d3.select(yAxis)
            .call(d3.axisLeft(yMapping).ticks(5))
            .call((g) => g.select(".domain").attr("stroke", "#d1d5db"))
            .call((g) => g.selectAll(".tick line").attr("stroke", "#e5e7eb"))
            .call((g) =>
                g
                    .selectAll(".tick text")
                    .attr("fill", "#6b7280")
                    .attr("font-size", "11px")
                    .attr("font-family", "inherit"),
            );
    });
</script>

<div bind:this={container} class="relative">
    <svg
        class="w-full h-auto block cursor-crosshair focus:outline-none"
        viewBox={`0 0 ${svgConfig.width} ${svgConfig.height}`}
        preserveAspectRatio="xMidYMin meet"
        role="img"
        aria-label="{xLabel} vs {yLabel}"
        onmouseover={() => (isHovered = true)}
        onmouseout={() => (isHovered = false)}
        onfocus={() => {}}
        onblur={() => {}}
        onmousemove={(evt) => {
            const svg = evt.currentTarget as SVGSVGElement;
            const rect = svg.getBoundingClientRect();
            const scaleX = svgConfig.width / rect.width;
            const scaleY = svgConfig.height / rect.height;
            const svgX = (evt.clientX - rect.left) * scaleX;
            const svgY = (evt.clientY - rect.top) * scaleY;
            mouseCoords = {
                x: xMapping.invert(svgX),
                y: yMapping.invert(svgY),
            };
        }}
        overflow="visible"
    >
        <!-- Subtle grid lines -->
        {#each xMapping.ticks(5) as tick}
            <line
                x1={xMapping(tick)}
                y1={svgConfig.marginTop}
                x2={xMapping(tick)}
                y2={svgConfig.height - svgConfig.marginBottom}
                stroke="#f3f4f6"
                stroke-width="1"
            />
        {/each}
        {#each yMapping.ticks(5) as tick}
            <line
                x1={svgConfig.marginLeft}
                y1={yMapping(tick)}
                x2={svgConfig.width - svgConfig.marginRight}
                y2={yMapping(tick)}
                stroke="#f3f4f6"
                stroke-width="1"
            />
        {/each}

        <g
            transform={`translate(0,${svgConfig.height - svgConfig.marginBottom})`}
            bind:this={xAxis}
        />
        <g
            transform={`translate(${svgConfig.marginLeft},0)`}
            bind:this={yAxis}
        />

        <!-- Axis labels -->
        <text
            x={svgConfig.width / 2}
            y={svgConfig.height - 4}
            fill="#9ca3af"
            font-size="12"
            font-family="inherit"
            text-anchor="middle">{xLabel}</text
        >
        <text
            fill="#9ca3af"
            font-size="12"
            font-family="inherit"
            text-anchor="middle"
            transform={`rotate(-90) translate(${-svgConfig.height / 2}, ${svgConfig.marginLeft / 3})`}
            >{yLabel}</text
        >

        {@render children()}
    </svg>

    {#if isHovered}
        <div
            class="absolute bottom-2 left-2 bg-white border border-gray-100
            text-gray-500 text-xs px-2 py-1 rounded-md pointer-events-none"
        >
            {mouseCoords.x.toFixed(2)}, {mouseCoords.y.toFixed(2)}
        </div>
    {/if}
</div>
