<script lang="ts">
    import * as d3 from "d3";
    import BehaviourComponent from "./Behaviour.svelte";

    const props = $props();
    const statement: Statement = props.statement as Statement;
    
    let statementElement: SVGGElement;
    let isHovered: boolean = $state(false);
    let isClicked: boolean = $state(false);
    const x = props.x as d3.ScaleLinear<number, number>; 
    const y = props.y as d3.ScaleLinear<number, number>;

    function calcBehaviourSize(st: Statement): number {
        return Math.min(
            x(st.domain.end) - x(st.domain.start),
            y(st.range.start) - y(st.range.end), 
            50
        ) * 0.8; 
    }
</script>

<g 
    onmouseover={() => isHovered = true}
    onmouseout={() => isHovered = false}
    onfocus={() => isClicked = true}
    onblur={() => isClicked = false}
    role="button"
    tabindex=0
    class="outline-none"
>
    <rect
        bind:this={statementElement} 
        width={x(statement.domain.end) - x(statement.domain.start)}
        height={y(statement.range.start) - y(statement.range.end)}
        x={x(statement.domain.start)}
        y={y(statement.range.end)}
        fill-opacity="0"
        class="stroke-black"
        class:stroke-sky-600={isHovered || isClicked}
    />

    <BehaviourComponent
        isHovered={isHovered || isClicked}
        behaviour={statement.behaviour.toLowerCase()}
        size={calcBehaviourSize(statement)}
        x={x(statement.domain.start) + (x(statement.domain.end) - x(statement.domain.start)) / 2}
        y={y(statement.range.end) + (y(statement.range.start) - y(statement.range.end)) / 2}
    />
</g>
