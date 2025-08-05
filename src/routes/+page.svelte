<script lang="ts">
    import GraphContainer from "$components/GraphContainer.svelte";
    import * as pts from "$lib/modules/points"
    import * as api from "$lib/modules/api";
    import { headerData } from "$lib/stores/headerData.svelte";

	let { data } = $props();
    const problems: ProblemData[] = $state(data.result);
    
    headerData.currentProblem = problems[3];
    headerData.normalise = async () => {problemData = await api.normalise(problemData)};
    headerData.solve = async () => {
        if (headerData.currentProblem != null) {
            points = pts.initialiseDefaultPoints(headerData.currentProblem);
        }
        points = await api.solve(problemData, headerData.solverType)
    };
    headerData.problems = problems;
    
    let points: Points = $state(pts.initialiseDefaultPoints(headerData.currentProblem));
    $effect(() => {
        if (headerData.currentProblem != null) {
            points = pts.initialiseDefaultPoints(headerData.currentProblem);
        }
    });
    
    let problemData = $derived(headerData.currentProblem);
    let scheme: Scheme = $derived(problemData.scheme);
    let hypothesis: Hypothesis = $derived(problemData.hypothesis);

</script>

<div 
    id="scheme-container"
    class="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 justify-center p-6 gap-6"
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
