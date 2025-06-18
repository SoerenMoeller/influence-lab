<script>
    import GraphContainer from "$components/GraphContainer.svelte";
	let { data } = $props();
</script>

<p>{data.result}</p>

<h1 
    class="flex justify-center mt-20 font-bold text-2xl"
>
    Work in Progress...
</h1>

<GraphContainer/>

