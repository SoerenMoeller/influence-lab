<script lang="ts">
    import BehaviourComponent from "./Behaviour.svelte";

    const props = $props();
    const statement: Statement = props.statement as Statement;
    
    let statementElement: SVGGElement;
    const x = props.x as d3.ScaleLinear<number, number>; 
    const y = props.y as d3.ScaleLinear<number, number>;

    function calcBehaviourSize(st: Statement): number {
        return Math.min(
            x(st.domain.end) - x(st.domain.start),
            y(st.range.start) - y(st.range.end), 
            50
        ) * 0.8; 
    }

    const outlineEffects = ['outline-2', 'outline-sky-600'];

    const handleMouseOver = (evt: MouseEvent | FocusEvent) => {
        evt.preventDefault();
        if (statementElement) {
            statementElement.classList.add(...outlineEffects);
        }
    };

    const handleMouseOut = (evt: MouseEvent | FocusEvent) => {
        evt.preventDefault();
        if (statementElement) {
            statementElement.classList.remove(...outlineEffects);
        }
    };
</script>

<g 
    bind:this={statementElement} 
    onmouseover={handleMouseOver}
    onmouseout={handleMouseOut}
    onfocus={handleMouseOver}
    onblur={handleMouseOut}
    aria-hidden="true"
    class="outline-none outline-offset-0"
>
    <rect
        width={x(statement.domain.end) - x(statement.domain.start)}
        height={y(statement.range.start) - y(statement.range.end)}
        x={x(statement.domain.start)}
        y={y(statement.range.end)}
        fill-opacity="0"
        stroke="black"
    />

    <BehaviourComponent
        behaviour={statement.behaviour.toLowerCase()}
        size={calcBehaviourSize(statement)}
        x={x(statement.domain.start) + (x(statement.domain.end) - x(statement.domain.start)) / 2}
        y={y(statement.range.end) + (y(statement.range.start) - y(statement.range.end)) / 2}
    />
</g>
