<script lang="ts">
    import GraphContainer from "$components/GraphContainer.svelte";
    import * as pts from "$lib/modules/points"
    import * as api from "$lib/modules/api";
    import * as headerActions from "$lib/stores/headerActions.svelte";

	let { data } = $props();
    const problems: ProblemData[] = $state(data.result);
    let problemIndex = 1; 

    let problemData = $state(problems[problemIndex]);
    let scheme: Scheme = $derived(problemData.scheme);
    let hypothesis: Hypothesis = $derived(problemData.hypothesis);
    let points: Points = $state(pts.initialiseDefaultPoints(data.result[problemIndex]));

    $effect(() => {
        points = pts.initialiseDefaultPoints(data.result[problemIndex]);
    });
    
    headerActions.setNormaliseAction(async () => {
        problemData = await api.normalise(problemData)
    })
    
    headerActions.setSolveAction(async () => {
        points = await api.solve(problemData)
    })
    
</script>

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
