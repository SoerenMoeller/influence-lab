<script lang="ts">
    import * as d3 from "d3";
    import StatementComponent from "$lib/components/statement/Statement.svelte";
    import SVGContainer from "./svgContainer.svelte";
    import CoordinateSystem from "./CoordinateSystem.svelte";
    import type { Scheme } from "$lib/types/scheme";
    import type { LongStatement } from "$lib/types/statement";

    import { svgConfig } from "$lib/modules/svgConfig";
    import { appState } from "$lib/stores/appState.svelte";
    import { getBoundaries } from "./boundaries";

    let { scheme, variableFrom, variableTo, hypothesis } = $props<{
        scheme: Scheme;
        variableFrom: string;
        variableTo: string;
        hypothesis: LongStatement | null;
    }>();

    const statements = $derived(
        scheme.statements.get(variableFrom)?.get(variableTo) ?? [],
    );

    const displayBounds = $derived({
        domain: getBoundaries(variableFrom, scheme, hypothesis),
        range: getBoundaries(variableTo, scheme, hypothesis),
    });

    const d3Scale = $derived({
        domain: d3
            .scaleLinear()
            .domain([displayBounds.domain.min, displayBounds.domain.max])
            .range([
                svgConfig.marginLeft,
                svgConfig.width - svgConfig.marginRight,
            ]),
        range: d3
            .scaleLinear()
            .domain([displayBounds.range.min, displayBounds.range.max])
            .range([
                svgConfig.height - svgConfig.marginBottom,
                svgConfig.marginTop,
            ]),
    });
</script>

<div class="bg-white border border-gray-100 rounded-xl p-4">
    <p
        class="text-[11px] font-medium text-gray-400 uppercase tracking-wide mb-2"
    >
        {variableFrom} → {variableTo}
    </p>

    <SVGContainer {d3Scale} {variableFrom} {variableTo}>
        <CoordinateSystem {d3Scale} {variableFrom} {variableTo} />

        {#each statements as st}
            <StatementComponent
                statement={{
                    domain: st.domain,
                    behaviour: st.behaviour,
                    range: st.range,
                    variableFrom: variableFrom,
                    variableTo: variableTo,
                }}
                {d3Scale}
                isHypothesis={false}
            />
        {/each}

        {#if appState.settings.showHypothesis && variableFrom == hypothesis.variableFrom && variableTo == hypothesis.variableTo}
            <StatementComponent
                statement={hypothesis}
                isHypothesis={true}
                {d3Scale}
            />
        {/if}
    </SVGContainer>
</div>
