<script lang="ts">
    import * as d3 from "d3";
    import { onMount } from "svelte";
    import { svgConfig } from "$lib/modules/svgConfig";

    let { variableFrom, variableTo, d3Scale } = $props();
    let xAxis: SVGGElement;
    let yAxis: SVGGElement;

    onMount(() => {
        d3.select(xAxis)
            .call(d3.axisBottom(d3Scale.domain).ticks(5))
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
            .call(d3.axisLeft(d3Scale.range).ticks(5))
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

{#each d3Scale.domain.ticks(5) as tick}
    <line
        x1={d3Scale.domain(tick)}
        y1={svgConfig.marginTop}
        x2={d3Scale.domain(tick)}
        y2={svgConfig.height - svgConfig.marginBottom}
        stroke="#f3f4f6"
        stroke-width="1"
    />
{/each}
{#each d3Scale.range.ticks(5) as tick}
    <line
        x1={svgConfig.marginLeft}
        y1={d3Scale.range(tick)}
        x2={svgConfig.width - svgConfig.marginRight}
        y2={d3Scale.range(tick)}
        stroke="#f3f4f6"
        stroke-width="1"
    />
{/each}

<g
    transform={`translate(0,${svgConfig.height - svgConfig.marginBottom})`}
    bind:this={xAxis}
/>
<g transform={`translate(${svgConfig.marginLeft},0)`} bind:this={yAxis} />

<!-- Axis labels -->
<text
    x={svgConfig.width / 2}
    y={svgConfig.height - 4}
    fill="#9ca3af"
    font-size="12"
    font-family="inherit"
    text-anchor="middle">{variableFrom}</text
>
<text
    fill="#9ca3af"
    font-size="12"
    font-family="inherit"
    text-anchor="middle"
    transform={`rotate(-90) translate(${-svgConfig.height / 2}, ${svgConfig.marginLeft / 3})`}
    >{variableTo}</text
>
