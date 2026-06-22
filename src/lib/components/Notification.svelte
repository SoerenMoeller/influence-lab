<script lang="ts">
    import { notifications } from "$lib/stores/notification.svelte";
    import { removeNotification } from "$lib/stores/notification.svelte";
    import { fly } from "svelte/transition";
    import Spinner from "./Spinner.svelte";

    const typeStyles = {
        success: {
            dot: "bg-teal-400",
            text: "text-teal-700",
            border: "border-teal-100",
        },
        error: {
            dot: "bg-red-400",
            text: "text-red-700",
            border: "border-red-100",
        },
        delay: {
            dot: "bg-amber-400",
            text: "text-amber-700",
            border: "border-amber-100",
        },
    };
</script>

<div
    class="fixed top-4 left-1/2 -translate-x-1/2 z-50 flex flex-col items-center gap-2"
>
    {#each notifications as notification (notification.id)}
        {@const s = typeStyles[notification.type]}
        <div
            in:fly={{ y: -16, duration: 250 }}
            out:fly={{ y: -16, duration: 200 }}
            class="flex items-center gap-3 pl-3 pr-2 py-2 rounded-lg bg-white
                border text-sm font-medium shadow-none min-w-48
                {s.border} {s.text}"
        >
            <span class="size-2 rounded-full shrink-0 {s.dot}"></span>

            <span class="flex-1">{notification.message}</span>

            {#if notification.type === "delay"}
                <Spinner />
            {/if}

            <button
                onclick={() => removeNotification(notification)}
                aria-label="Close notification"
                class="ml-1 text-current opacity-40 hover:opacity-70 transition-opacity
                    text-base leading-none"
            >
                ×
            </button>
        </div>
    {/each}
</div>
