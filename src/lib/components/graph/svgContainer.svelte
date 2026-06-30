<script lang="ts">
    import { svgConfig } from "$lib/modules/svgConfig";
    import { appState } from "$lib/stores/appState.svelte";
    import StatementOverlay from "./StatementOverlay.svelte";

    let container: HTMLDivElement;
    let { children, d3Scale, variableFrom, variableTo } = $props();

    let isHovered = $state(false);
    let mouseCoords = $state({ x: 0, y: 0 });
</script>

<div bind:this={container} class="relative">
    <svg
        class="w-full h-auto block cursor-crosshair focus:outline-none"
        viewBox={`0 0 ${svgConfig.width} ${svgConfig.height}`}
        preserveAspectRatio="xMidYMin meet"
        role="img"
        aria-label="influence of {variableFrom} onto {variableTo}"
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
                x: d3Scale.domain.invert(svgX),
                y: d3Scale.range.invert(svgY),
            };
        }}
        overflow="visible"
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

    {#if appState.highlightedStatement && appState.highlightedStatement.variableFrom === variableFrom && appState.highlightedStatement.variableTo === variableTo}
        <StatementOverlay statement={appState.highlightedStatement} />
    {/if}
</div>
