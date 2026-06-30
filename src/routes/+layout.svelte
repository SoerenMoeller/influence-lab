<script lang="ts">
    import "../app.css";
    import type { Snippet } from "svelte";
    import type { LayoutData } from "./$types";
    import { appState } from "$lib/stores/appState.svelte";
    import Header from "$lib/components/header/Header.svelte";
    import Notification from "$lib/components/Notification.svelte";

    let { data, children }: { data: LayoutData; children: Snippet } = $props();

    $effect(() => {
        appState.problemPool = data.problems;
        appState.restoreFromStorage();
    });

    $effect(() => {
        appState.selectedProblemIndex;
        appState.isShowingNormalised;
        appState.settings.showHypothesis;
        appState.persist();
    });
</script>

<div class="bg-gray-50 min-h-screen">
    <Header />
    <Notification />

    {@render children()}
</div>
