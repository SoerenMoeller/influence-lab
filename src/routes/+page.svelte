<script lang="ts">
    import { appState } from "$lib/stores/appState.svelte";
    import { normalise } from "$lib/modules/api";
    import type { Scheme } from "$lib/types/scheme";
    import GraphContainer from "$components/graph/GraphContainer.svelte";

    let activeScheme = $state(0);
    let schemeTabs = $derived(
        appState.problem
            ? appState.problem.schemeVersions.map((version, i) => ({
                  label: `Scheme ${i + 1}`,
                  index: i,
                  scheme: version,
              }))
            : [],
    );

    const scheme: Scheme | null = $derived.by(() => {
        if (schemeTabs.length === 0) return null;
        const active = schemeTabs[activeScheme];
        if (!appState.isShowingNormalised) return active.scheme;
        return appState.normalisedProblem?.schemeVersions[active.index] ?? null;
    });

    let normalising = false;

    $effect(() => {
        if (
            appState.isShowingNormalised &&
            appState.normalisedProblem == null &&
            !normalising
        ) {
            normalising = true;
            normalise(appState.problem).then((normalised) => {
                appState.normalisedProblem = normalised;
                normalising = false;
            });
        }
    });
</script>

{#if schemeTabs.length == 0}
    <div class="flex items-center justify-center h-48 text-gray-500">
        No problem selected. Please select a problem from the header.
    </div>
{:else}
    <div class="flex border-b border-gray-200 mb-4 gap-2">
        {#each schemeTabs as tab}
            <button
                type="button"
                class="px-4 py-2 text-sm font-medium transition-colors border-b-2 -mb-[2px]
            {activeScheme === tab.index
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}"
                onclick={() => (activeScheme = tab.index)}
            >
                {tab.label}
            </button>
        {/each}
    </div>

    {#if scheme != null}
        <div class="grid grid-cols-2 justify-center p-6 gap-6">
            {#each [...scheme.statements] as [variableFrom, innerMap]}
                {#each [...innerMap] as [variableTo, sts]}
                    <GraphContainer
                        {variableFrom}
                        {variableTo}
                        {scheme}
                        hypothesis={appState.problem?.hypothesis}
                    />
                {/each}
            {/each}
        </div>
    {/if}
{/if}
