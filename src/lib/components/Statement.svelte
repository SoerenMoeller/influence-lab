<script lang="ts">
    import * as d3 from "d3";
    import BehaviourComponent from "./Behaviour.svelte";

    const props = $props();
    const statement: Statement = props.statement as Statement;
    const highlighted: boolean  = props.highlighted as boolean;
    
    let statementElement: SVGGElement;
    let isHovered: boolean = $state(false);
    let isClicked: boolean = $state(false);
    const xMapping = props.xMapping as d3.ScaleLinear<number, number>; 
    const yMapping = props.yMapping as d3.ScaleLinear<number, number>;

    function calcBehaviourSize(st: Statement): number {
        return Math.min(
            xMapping(st.domain.end) - xMapping(st.domain.start),
            yMapping(st.range.start) - yMapping(st.range.end), 
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
        width={xMapping(statement.domain.end) - xMapping(statement.domain.start)}
        height={yMapping(statement.range.start) - yMapping(statement.range.end)}
        x={xMapping(statement.domain.start)}
        y={yMapping(statement.range.end)}
        fill-opacity="0"
        class="stroke-black"
        class:stroke-red-700={highlighted}
        class:stroke-sky-600={isHovered || isClicked}
    />

    <BehaviourComponent
        isHovered={isHovered || isClicked}
        behaviour={statement.behaviour.toLowerCase()}
        {highlighted}
        size={calcBehaviourSize(statement)}
        x={xMapping(statement.domain.start) + (xMapping(statement.domain.end) - xMapping(statement.domain.start)) / 2}
        y={yMapping(statement.range.end) + (yMapping(statement.range.start) - yMapping(statement.range.end)) / 2}
    />
</g>
