<script lang="ts">
    import "../app.css";
    import { normaliseButtonAction, solveButtonAction } from '$lib/stores/headerActions.svelte';
    import Notification from "$components/Notification.svelte";
    
    let { children } = $props();
    const normalise = $derived(normaliseButtonAction.action);
    const solver = $derived(solveButtonAction.action);
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
            {@render button(normalise, 'Normalise')}
            {@render button(solver, 'Solve')}
        </div>
    </header>

    <Notification />

    {@render children()}
</div> 
