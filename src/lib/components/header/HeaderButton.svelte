<script lang="ts">
    import type { Snippet } from "svelte";

    type Props = {
        onclick: () => void;
        label: string;
        colorClass?: string;
        children?: Snippet;
    };
    let { onclick, label, children, colorClass = "" }: Props = $props();
</script>

<button
    {onclick}
    class="flex items-center gap-1.5 h-9 min-w-36 px-4 text-sm font-medium rounded-lg border
    transition-colors justify-center {colorClass}"
>
    {@render children?.()}
    {label}
</button>
