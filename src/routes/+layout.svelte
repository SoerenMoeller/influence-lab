<script lang="ts">
    import "../app.css";
    import { headerData } from '$lib/stores/headerData.svelte';
    import Notification from "$components/Notification.svelte";
    
    let { children } = $props();
</script>

{#snippet button(callback: (evt: MouseEvent) => void, name: string)}
    <button 
        onclick={callback}
        class="bg-sky-700 hover:bg-sky-600 text-center px-6 py-2 
            rounded-lg w-48 text-lg text-white font-semibold 
            border border-black"
    >
        {name}
    </button>
{/snippet}

<div class="bg-gray-100 min-h-screen">
    <header 
        class="flex items-center justify-between p-6 bg-sky-100 h-30 shadow-md"
    >
        <h3 class="font-semibold text-3xl text-sky-900">
            Influence Lab
        </h3>
        <div class="flex gap-4">
            <select 
                name="problem" 
                id="problem"
                class="w-48 text-center border border-black rounded-lg bg-white"
                bind:value={headerData.currentProblem}
            >
                {#each headerData.problems as problem, index}
                    <option value={problem}>
                        {`Problem ${index + 1}`}
                    </option>
                {/each}
            </select>
            {@render button(headerData.normalise, 'Normalise')}
            {@render button(headerData.solve, 'Solve')}
            <select 
                name="solver" 
                id="solver"
                class="w-48 text-center border border-black rounded-lg bg-white"
                bind:value={headerData.solverType}
            >
                {#each ['sat', 'uninterpreted', 'integer', 'array', 'incremental'] as solverType}
                    <option 
                        value={solverType}
                    >
                        {solverType}
                    </option>
                {/each}
            </select>
        </div>
    </header>

    <Notification />

    {@render children()}
</div> 
