<script lang="ts">
    import BehaviourComponent from "./Behaviour.svelte";
    import { appState } from "$lib/stores/appState.svelte";
    import { equalLongStatements } from "$lib/types/statement";

    let { statement, isHypothesis, d3Scale } = $props();

    let statementElement: SVGGElement;
    let isHovered: boolean = $state(false);
    const isHighlighted = $derived(
        equalLongStatements(appState.highlightedStatement, statement),
    );

    const statementBounds = $derived({
        domain: {
            start: d3Scale.domain(statement.domain.start),
            width: Math.max(
                d3Scale.domain(statement.domain.end) -
                    d3Scale.domain(statement.domain.start),
                1,
            ),
            center: d3Scale.domain(
                (statement.domain.start + statement.domain.end) / 2,
            ),
        },
        range: {
            start: d3Scale.range(statement.range.end),
            height: Math.max(
                d3Scale.range(statement.range.start) -
                    d3Scale.range(statement.range.end),
                1,
            ),
            center: d3Scale.range(
                (statement.range.start + statement.range.end) / 2,
            ),
        },
    });

    const color = $derived({
        fill: (() => {
            if (!isHypothesis) {
                return isHighlighted || isHovered ? "#EFF6FF" : "transparent";
            } else {
                return isHighlighted || isHovered ? "#F08D8D" : "#EDCCCC";
            }
        })(),
        stroke: (() => {
            if (!isHypothesis) {
                return isHighlighted || isHovered ? "#3B82F6" : "#D1D5DB";
            } else {
                return "#DC2626";
            }
        })(),
    });

    function calcBehaviourSize(width: number, height: number): number {
        return Math.min(width, height, 50) * 0.8;
    }
</script>

<g
    role="button"
    tabindex="0"
    aria-label={`Statement: ${statement.behaviour} from ${statement.variableFrom} to ${statement.variableTo}`}
    onmouseover={() => (isHovered = true)}
    onmouseout={() => (isHovered = false)}
    onfocus={() => (isHovered = true)}
    onblur={() => (isHovered = false)}
    onclick={(e) => {
        if (equalLongStatements(appState.highlightedStatement, statement)) {
            appState.highlightedStatement = null;
        } else {
            appState.highlightedStatement = statement;
        }
    }}
    onkeydown={(event) => {
        if (event.key === "Enter" || event.key === " ") {
            if (equalLongStatements(appState.highlightedStatement, statement)) {
                appState.highlightedStatement = null;
            } else {
                appState.highlightedStatement = statement;
            }
        }
    }}
    class="outline-none cursor-pointer"
>
    <!-- Hover fill -->
    <rect
        x={statementBounds.domain.start}
        y={statementBounds.range.start}
        width={statementBounds.domain.width}
        height={statementBounds.range.height}
        fill={color.fill}
        opacity={0.4}
        stroke="none"
        rx="2"
    />

    <!-- Border -->
    <rect
        bind:this={statementElement}
        x={statementBounds.domain.start}
        y={statementBounds.range.start}
        width={statementBounds.domain.width}
        height={statementBounds.range.height}
        fill="none"
        rx="2"
        stroke={color.stroke}
        stroke-width={isHighlighted || isHovered ? 1.5 : 1}
    />

    <!-- Behaviour icon -->
    <BehaviourComponent
        {isHighlighted}
        {isHypothesis}
        behaviour={statement.behaviour.toLowerCase()}
        size={calcBehaviourSize(
            statementBounds.domain.width,
            statementBounds.range.height,
        )}
        x={statementBounds.domain.center}
        y={statementBounds.range.center}
    />
</g>
