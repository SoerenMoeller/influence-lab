<script lang="ts">
    import * as d3 from "d3";
    import { onMount } from "svelte";

    let container: HTMLDivElement;
    let { scheme } = $props();
        
    // Declare the chart dimensions and margins.
    const width = 1080;
    const height = 720;
    const marginTop = 20;
    const marginRight = 20;
    const marginBottom = 30;
    const marginLeft = 40;

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

    onMount(() => {
        // Create the SVG container.
        const svg = d3.create("svg")
            .attr("width", width)
            .attr("height", height);

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
        //svg.append("rect")
        //    .attr("width", 20)
        //    .attr("height", 20)
        //    .attr("x", 200)
        //    .attr("y", 20)
        //    .attr("fill-opacity", 0)
        //    .attr("stroke", "black");

        //gy.transition()
        //    .duration(750)
        //    .call(d3.axisLeft(y));
            
        // Append the SVG element.
        container.append(svg.node());
    });
</script>

<div 
    bind:this={container}
    class="flex w-full justify-center items-center"></div>
