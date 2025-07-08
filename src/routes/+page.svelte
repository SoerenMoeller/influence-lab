<script lang="ts">
    import GraphContainer from "$components/GraphContainer.svelte";
    import Notification from "$components/Notification.svelte";
    import * as io from "$lib/modules/scheme/io";
    import { showNotification } from "$lib/stores/notification.js";
    
	let { data } = $props();
    let scheme: Scheme = $state(data.result) as Scheme;
    let points: Points = $state(new Map);


    showNotification("Scheme loaded successfully.", "success");

    const runNormalisation = async (evt: MouseEvent) => {
        evt.preventDefault();

        const listScheme = io.schemeToStatementList(scheme);
        const res = await fetch('/api/normalise', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(listScheme)
        });

        if (!res.ok) {
            console.error("Failed to normalise:", await res.text());
            showNotification("Scheme could not be normalised.", "error");
            return;
        }

        const normalised = await res.json();
        const normalisedScheme = io.statementListToScheme(normalised);
        
        scheme = normalisedScheme;
     
        showNotification("Scheme successfully normalised.", "success");
    }
    
    const runSolver = async (evt: MouseEvent) => {
        evt.preventDefault();

        const listScheme = io.schemeToStatementList(scheme);
        const res = await fetch('/api/solver', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(listScheme)
        });

        if (!res.ok) {
            console.error("Failed to solve:", await res.text());
            showNotification("Scheme could not be solved.", "error");
            return;
        }

        points = await res.json() as Points;
     
        showNotification("Scheme successfully solved.", "success");
    }
</script>

<header 
    class="flex items-center justify-between p-6 bg-sky-100 h-30 shadow-md"
>
    <h3 class="font-semibold text-3xl text-sky-900">
        Influence Lab
    </h3>
    <div class="flex gap-4">
        <button 
            onclick={runNormalisation}
            class="bg-sky-700 hover:bg-sky-600 text-center px-6 py-2 
                rounded-lg w-48 text-lg text-white font-semibold 
                border border-black"
        >
            Normalise 
        </button>
        <button 
            onclick={runSolver}
            class="bg-sky-700 hover:bg-sky-600 text-center px-6 py-2 
                rounded-lg w-48 text-lg text-white font-semibold 
                border border-black"
        >
            Solve 
        </button>
    </div>
</header>

<Notification />

<div 
    id="scheme-container"
    class="grid grid-cols-1 lg:grid-cols-2 justify-center p-6 gap-6"
>
    {#key scheme}
        {#each [...scheme] as [variableFrom, innerMap]}
            {#each [...innerMap] as [variableTo, statements]}
                <GraphContainer 
                    {variableFrom}
                    {variableTo}
                    scheme={statements}
                    points={}
                />
            {/each}
        {/each}
    {/key} 
</div>

<style>
</style>
