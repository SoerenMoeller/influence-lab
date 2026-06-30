<script lang="ts">
    import { getSettingsForBehaviour } from "./behaviourSettings";

    let { isHighlighted, isHypothesis, behaviour, size, x, y } = $props();
    const settings = $derived(getSettingsForBehaviour(behaviour));

    const clampedSize = $derived(Math.min(size, 24));
    const width = $derived(clampedSize);
    const height = $derived(clampedSize);
    const adjustedX = $derived(x - width / 2);
    const adjustedY = $derived(y - height / 2);
</script>

<svg
    xmlns="http://www.w3.org/2000/svg"
    {width}
    {height}
    viewBox={settings.viewBox}
    xmlns:xlink="http://www.w3.org/1999/xlink"
    aria-hidden="true"
    x={adjustedX}
    y={adjustedY}
>
    <defs>
        <path id={settings.id} d={settings.drawPath}> </path>
    </defs>
    <g
        class="fill-black stroke-black"
        class:fill-sky-600={isHighlighted && !isHypothesis}
        class:stroke-sky-600={isHighlighted && !isHypothesis}
        class:fill-red-700={isHypothesis}
        class:stroke-red-700={isHypothesis}
        stroke-width="0"
        transform="scale(1,-1)"
    >
        <g data-mml-node="math">
            <g data-mml-node="mo">
                <use xlink:href={`#${settings.id}`}> </use>
            </g>
        </g>
    </g>
</svg>
