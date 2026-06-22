<script lang="ts">
    import * as d3 from "d3";
    import BehaviourComponent from "./Behaviour.svelte";

    let {
        statement,
        highlighted,
        xMapping,
        yMapping,
        variableFrom,
        variableTo,
    } = $props<{
        statement: Statement;
        highlighted: boolean;
        xMapping: d3.ScaleLinear<number, number>;
        yMapping: d3.ScaleLinear<number, number>;
        variableFrom: string;
        variableTo: string;
    }>();

    let statementElement: SVGGElement;
    let isHovered: boolean = $state(false);
    let isClicked: boolean = $state(false);

    const x = $derived(xMapping(statement.domain.start));
    const y = $derived(yMapping(statement.range.end));
    const width = $derived(
        Math.max(
            xMapping(statement.domain.end) - xMapping(statement.domain.start),
            1,
        ),
    );
    const height = $derived(
        Math.max(
            yMapping(statement.range.start) - yMapping(statement.range.end),
            1,
        ),
    );
    const cx = $derived(x + width / 2);
    const cy = $derived(y + height / 2);

    function calcBehaviourSize(): number {
        return Math.min(width, height, 50) * 0.8;
    }
</script>

<g
    role="button"
    tabindex="0"
    aria-label={`Statement: ${statement.behaviour} from ${variableFrom} to ${variableTo}`}
    onmouseover={() => (isHovered = true)}
    onmouseout={() => (isHovered = false)}
    onfocus={() => (isHovered = true)}
    onblur={() => (isHovered = false)}
    onclick={(event) => {
        isClicked = !isClicked;
    }}
    onkeydown={(event) => {
        if (event.key === "Enter" || event.key === " ") {
            isClicked = !isClicked;
        }
    }}
    class="outline-none cursor-pointer"
>
    <!-- Hover fill -->
    <rect
        {x}
        {y}
        {width}
        {height}
        fill={isHovered || isClicked
            ? highlighted
                ? "#FEF2F2"
                : "#EFF6FF"
            : "transparent"}
        stroke="none"
        rx="2"
    />

    <!-- Border -->
    <rect
        bind:this={statementElement}
        {x}
        {y}
        {width}
        {height}
        fill="none"
        rx="2"
        stroke={highlighted
            ? "#DC2626"
            : isHovered || isClicked
              ? "#3B82F6"
              : "#D1D5DB"}
        stroke-width={highlighted ? 1.5 : 1}
    />

    <!-- Behaviour icon -->
    <BehaviourComponent
        isHovered={isHovered || isClicked}
        behaviour={statement.behaviour.toLowerCase()}
        {highlighted}
        size={calcBehaviourSize()}
        x={cx}
        y={cy}
    />
</g>

<!-- ✅ Move foreignObject OUTSIDE the <g> -->
{#if isClicked}
    <foreignObject
        x={cx - 200}
        y={cy - 50}
        width="400"
        height="100"
        style="position: absolute; top: 0; left: 0; pointer-events: none;"
    >
        <div
            xmlns="http://www.w3.org/1999/xhtml"
            class="flex justify-center items-center w-full h-full"
        >
            <div
                class="bg-white border border-gray-100 rounded-lg shadow-sm
                    px-4 py-3 text-xl text-gray-700 whitespace-nowrap
                    max-w-full"
                style="box-sizing: border-box;"
            >
                <span class="font-semibold text-gray-900">{variableFrom}</span>
                <span class="text-gray-400 mx-1">●</span>
                <span class="text-gray-500"
                    >[{statement.domain.start}, {statement.domain.end}]</span
                >
                <span
                    class="font-medium text-gray-600"
                    aria-label={statement.behaviour}
                    tabindex="-1"
                    style="font-family: system-ui, sans-serif; font-size: 1.2em;"
                >
                    {#if statement.behaviour.toLowerCase() === "mono"}
                        ↗
                    {:else if statement.behaviour.toLowerCase() === "anti"}
                        ↘
                    {:else if statement.behaviour.toLowerCase() === "arb"}
                        ↝
                    {:else if statement.behaviour.toLowerCase() === "const"}
                        →
                    {:else}
                        {statement.behaviour}
                    {/if}
                </span>
                <span class="text-gray-500"
                    >[{statement.range.start}, {statement.range.end}]</span
                >
                <span class="text-gray-400 mx-1">●</span>
                <span class="font-semibold text-gray-900">{variableTo}</span>
            </div>
        </div>
    </foreignObject>
{/if}
