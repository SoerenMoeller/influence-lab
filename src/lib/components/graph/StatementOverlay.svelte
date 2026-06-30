<script lang="ts">
    import type { LongStatement } from "$lib/types/statement";

    const { statement } = $props<{ statement: LongStatement }>();
</script>

<div
    class="flex justify-center items-center absolute top-4 right-4 pointer-events-none"
>
    <div
        class="bg-white border border-gray-100 rounded-lg shadow-sm px-4 py-3 text-xl text-gray-700 whitespace-nowrap max-w-full"
        style="box-sizing: border-box;"
    >
        <span class="font-semibold text-gray-900">{statement.variableFrom}</span
        >
        <span class="text-gray-400 mx-1">●</span>
        <span class="text-gray-500"
            >[{statement.domain.start.toFixed(2)}, {statement.domain.end.toFixed(
                2,
            )}]</span
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
            >[{statement.range.start.toFixed(2)}, {statement.range.end.toFixed(
                2,
            )}]</span
        >
        <span class="text-gray-400 mx-1">●</span>
        <span class="font-semibold text-gray-900">{statement.variableTo}</span>
    </div>
</div>
