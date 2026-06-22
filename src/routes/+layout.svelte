<script lang="ts">
    import "../app.css";
    import { headerData, saveToStorage } from "$lib/stores/headerData.svelte";
    import Notification from "$components/Notification.svelte";
    let { children } = $props();

    $effect(() => {
        // Runs whenever these values change
        headerData.showHypothesis;
        headerData.currentProblem;
        saveToStorage();
    });
</script>

{#snippet button(callback: (evt: MouseEvent) => void, name: string)}
    <button
        onclick={callback}
        class="flex items-center gap-1.5 h-9 px-4 text-sm font-medium
            rounded-lg bg-sky-700 hover:bg-sky-600 text-sky-50
            border border-sky-700 transition-colors"
    >
        <svg
            xmlns="http://www.w3.org/2000/svg"
            class="size-4"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            ><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path
                d="M6 21l15 -15l-3 -3l-15 15l3 3"
            /><path d="M15 6l3 3" /><path
                d="M9 3a2 2 0 0 0 2 2a2 2 0 0 0 -2 2a2 2 0 0 0 -2 -2a2 2 0 0 0 2 -2"
            /></svg
        >
        {name}
    </button>
{/snippet}

<div class="bg-gray-50 min-h-screen">
    <header
        class="flex items-center justify-between px-6 h-16 bg-white border-b border-gray-200"
    >
        <div class="flex items-center gap-2.5">
            <div
                class="size-8 rounded-lg bg-sky-700 flex items-center justify-center"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="size-4 text-sky-100"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    ><path
                        d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v18m0 0h10a2 2 0 0 0 2-2v-4M9 21H5a2 2 0 0 1-2-2v-4m0 0h18"
                    /></svg
                >
            </div>
            <span class="text-[17px] font-medium text-gray-900 tracking-tight"
                >Influence Lab</span
            >
        </div>
        <div class="flex items-center gap-2.5">
            <div class="relative">
                <select
                    name="problem"
                    id="problem"
                    class="appearance-none h-9 pl-3 pr-8 text-sm rounded-lg
                        border border-gray-200 bg-white text-gray-800
                        hover:border-gray-300 focus:outline-none focus:ring-2
                        focus:ring-sky-500/30 cursor-pointer"
                    bind:value={headerData.currentProblem}
                >
                    {#each headerData.problems as problem, index}
                        <option value={problem}>Problem {index + 1}</option>
                    {/each}
                </select>
                <svg
                    class="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2 size-3.5 text-gray-400"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"><path d="m6 9 6 6 6-6" /></svg
                >
            </div>
            {@render button(headerData.normalise, "Normalise")}
            <button
                onclick={() =>
                    (headerData.showHypothesis = !headerData.showHypothesis)}
                class="flex items-center gap-1.5 h-9 px-4 text-sm font-medium
                rounded-lg border transition-colors
                {headerData.showHypothesis
                    ? 'bg-red-50 border-red-200 text-red-700 hover:bg-red-100'
                    : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'}"
            >
                <i
                    class="ti {headerData.showHypothesis
                        ? 'ti-eye-off'
                        : 'ti-eye'} text-sm"
                    aria-hidden="true"
                ></i>
                Hypothesis
            </button>
        </div>
    </header>
    <Notification />
    {@render children()}
</div>
