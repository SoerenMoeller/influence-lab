<script lang="ts">
    import { appState } from "$lib/stores/appState.svelte";

    let open = $state(false);
    let triggerEl: HTMLButtonElement;

    function select(index: number) {
        if (index != appState.selectedProblemIndex) {
            appState.normalisedProblem = null;
        }
        appState.selectedProblemIndex = index;
        open = false;
    }

    function onkeydown(e: KeyboardEvent) {
        if (e.key === "Escape") open = false;
    }

    function clickoutside(node: HTMLElement) {
        function handle(e: MouseEvent) {
            if (!node.contains(e.target as Node)) open = false;
        }
        document.addEventListener("mousedown", handle);
        return {
            destroy() {
                document.removeEventListener("mousedown", handle);
            },
        };
    }
</script>

<div class="relative" use:clickoutside>
    <button
        bind:this={triggerEl}
        onclick={() => (open = !open)}
        {onkeydown}
        class="flex items-center gap-1.5 h-9 min-w-36 px-4 text-sm font-medium rounded-lg border
            border-gray-200 bg-white text-gray-800 hover:border-gray-300
            focus:outline-none focus:ring-2 focus:ring-sky-500/30
            transition-colors justify-between cursor-pointer"
    >
        <span>Problem {appState.selectedProblemIndex + 1}</span>
        <svg
            class="size-3.5 text-gray-400 transition-transform {open
                ? 'rotate-180'
                : ''}"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
        >
            <path d="m6 9 6 6 6-6" />
        </svg>
    </button>

    {#if open}
        <ul
            class="absolute z-50 mt-1 w-full rounded-lg border border-gray-200 bg-white
                shadow-md overflow-hidden text-sm"
            role="listbox"
        >
            {#each appState.problemPool as _, index}
                <li
                    role="option"
                    aria-selected={appState.selectedProblemIndex === index}
                    onclick={() => select(index)}
                    onkeydown={(e) => e.key === "Enter" && select(index)}
                    tabindex="0"
                    class="flex items-center h-9 px-4 font-medium cursor-pointer
                        transition-colors
                        {appState.selectedProblemIndex === index
                        ? 'bg-sky-50 text-sky-600'
                        : 'text-gray-800 hover:bg-gray-50'}"
                >
                    Problem {index + 1}
                </li>
            {/each}
        </ul>
    {/if}
</div>
