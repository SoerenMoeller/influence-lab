<script lang="ts">
    import GraphContainer from "$components/GraphContainer.svelte";
    import Notification from "$components/Notification.svelte";
    import * as transform from "$lib/modules/transform";
    import { showNotification } from "$lib/stores/notification.js";
    
	let { data } = $props();
    let problemData: ProblemData = $state(data.result) as ProblemData;
    let scheme: Scheme = $derived(problemData.scheme);
    let hypothesis: Hypothesis = $derived(problemData.hypothesis);

    const initialPoints: Points = new Map();
    for (const [from, toSet] of data.result.scheme.order) {
        if (!initialPoints.has(from)) {
            initialPoints.set(from, new Map());
        }

        const innerMap = initialPoints.get(from)!;
        for (const to of toSet) {
            innerMap.set(to, []);  // Initialize with empty list
        }
    }
    let points: Points = $state(initialPoints);
    
    showNotification("Scheme loaded successfully.", "success");

    const runNormalisation = async (evt: MouseEvent) => {
        evt.preventDefault();

        const problemDataSer = transform.serialiseProblemData(problemData);
        const res = await fetch('/api/normalise', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(problemDataSer)
        });

        if (!res.ok) {
            console.error("Failed to normalise:", await res.text());
            showNotification("Scheme could not be normalised.", "error");
            return;
        }

        const normalisedProblem = await res.json();
        problemData = transform.deserialiseProblemData(normalisedProblem);
     
        showNotification("Scheme successfully normalised.", "success");
    }
    
    const runSolver = async (evt: MouseEvent) => {
        evt.preventDefault();

        const listScheme = transform.serialiseScheme(scheme);
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

        const result = await res.json();
        points = transform.deserializePoints(result);
     
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
    {#key problemData}
        {#each [...scheme.statements] as [variableFrom, innerMap]}
            {#each [...innerMap] as [variableTo, statements]}
                <GraphContainer 
                    {variableFrom}
                    {variableTo}
                    {hypothesis}
                    {scheme}
                    points={points.get(variableFrom)?.get(variableTo)}
                />
            {/each}
        {/each}
    {/key} 
</div>

<style>
</style>
