<script lang="ts">
    import { appState } from "$lib/stores/appState.svelte";
    import Icon from "./Icon.svelte";
    import HeaderButton from "./HeaderButton.svelte";
    import ProblemSelect from "./ProblemSelect.svelte";
</script>

<header
    class="flex items-center justify-between px-6 h-16 bg-white border-b border-gray-200"
>
    <div class="flex items-center gap-2.5">
        <Icon />
        <span class="text-[17px] font-medium text-gray-900 tracking-tight"
            >Influence Lab</span
        >
    </div>

    <div class="flex items-center gap-2.5">
        <ProblemSelect />
        <HeaderButton
            onclick={() =>
                (appState.isShowingNormalised = !appState.isShowingNormalised)}
            label={appState.isShowingNormalised ? "Original" : "Normalise"}
            colorClass="bg-sky-700 hover:bg-sky-600 text-sky-50 border-sky-700"
        />
        <HeaderButton
            onclick={() =>
                (appState.settings.showHypothesis =
                    !appState.settings.showHypothesis)}
            label="Hypothesis"
            colorClass="bg-red-50 border-red-200 text-red-700 hover:bg-red-100 active:bg-red-200"
        >
            <i
                class="ti {appState.settings.showHypothesis
                    ? 'ti-eye-off'
                    : 'ti-eye'} text-sm"
                aria-hidden="true"
            ></i>
        </HeaderButton>
    </div>
</header>
