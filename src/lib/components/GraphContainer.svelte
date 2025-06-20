<script lang="ts">
    import * as d3 from "d3";
    import { onMount } from "svelte";

    let container: HTMLDivElement;
    let { scheme } = $props();
    
    const map: Map<string, Map<string, Scheme>> = new Map<string, Map<string, Scheme>>();
    for (const st of scheme) {
        if (!map.has(st.variableFrom)) {
            map.set(st.variableFrom, new Map<string, Scheme>());
        }
        if (!map.get(st.variableFrom)!.has(st.variableTo)) {
            map.get(st.variableFrom)!.set(st.variableTo, []);
        }
        map.get(st.variableFrom)!.get(st.variableTo)!.push(st);
    }
        
    // Declare the chart dimensions and margins.
    function createPlot(variableFrom: string, variableTo: string, scheme: Scheme) {
        const width = 1080;
        const height = 720;
        const marginTop = 10;
        const marginRight = 20;
        const marginBottom = 80;
        const marginLeft = 80;

        const minValueDomain = Math.min(...scheme.map((st: Statement) => st.domain.start));
        const maxValueDomain = Math.max(...scheme.map((st: Statement) => st.domain.end));
        const minValueRange = Math.min(...scheme.map((st: Statement) => st.range.start));
        const maxValueRange = Math.max(...scheme.map((st: Statement) => st.range.end));

        // Declare the x (horizontal position) scale.
        const x = d3.scaleLinear()
            .domain([minValueDomain - 1, maxValueDomain + 1])
            .range([marginLeft, width - marginRight]);

        // Declare the y (vertical position) scale.
        const y = d3.scaleLinear()
            .domain([minValueRange - 1, maxValueRange + 1])
            .range([height - marginBottom, marginTop]);
            
        // Create the SVG container.
        const svg = d3.create("svg")
            .attr("viewBox", `0 0 ${width} ${height}`)
            .attr("preserveAspectRatio", "xMidYMin meet")
            .attr("class", "w-full h-auto block");

        // Add the x-axis.
        svg.append("g")
            .attr("transform", `translate(0,${height - marginBottom})`)
            .call(d3.axisBottom(x));

        // Add the y-axis.
        svg.append("g")
            .attr("transform", `translate(${marginLeft},0)`)
            .call(d3.axisLeft(y));

        for (const st of scheme) {
            svg.append("rect")
                .attr("width", x(st.domain.end) - x(st.domain.start))
                .attr("height", y(st.range.start) - y(st.range.end))
                .attr("x", x(st.domain.start))
                .attr("y", y(st.range.end))
                .attr("fill-opacity", 0)
                .attr("stroke", "black");

            svg.append("image")
                .attr("href", `/${st.behaviour.toLowerCase()}.svg`)
                .attr("width", 30)
                .attr("height", 30)
                .attr("x", x(st.domain.start) + (x(st.domain.end) - x(st.domain.start)) / 2 - 15)
                .attr("y", y(st.range.end) + (y(st.range.start) - y(st.range.end)) / 2 - 15);
        }

        svg.append("text")
            .attr("x", marginLeft)
            .attr("y", height / 2)
            .attr("fill", "black")
            .attr("font-size", "24px")
            .attr("transform", `rotate(-90, ${marginLeft / 2}, ${height / 2})`)
            .text(variableTo)

        svg.append("text")
            .attr("x", width / 2)
            .attr("y", height - marginBottom / 2)
            .attr("fill", "black")
            .attr("font-size", "24px")
            .text(variableFrom);

        // Append the SVG element.
        container.append(svg.node() as Node);
    }

    onMount(() => {
        for (const [variableFrom, map2] of map) {
            for (const [variableTo, subScheme] of map2) {
                createPlot(variableFrom, variableTo, subScheme);
            }
        }
    });
</script>

<div 
    bind:this={container}
    class="w-full"
>
</div>
