<script lang="ts">
    import { notifications } from '$lib/stores/notification.svelte';
    import { removeNotification } from '$lib/stores/notification.svelte';
    import { fly } from 'svelte/transition';
    import Spinner from './Spinner.svelte';
</script>

{#key notifications}
    <div class="fixed top-4 left-1/2 -translate-x-1/2 z-50 space-y-2">
        {#each notifications as notification (notification.id)}
            <div		
                in:fly={{ y: -100, duration: 500 }}
                out:fly={{ y: -100, duration: 500 }} 
                class="px-4 py-2 rounded shadow bg-white border text-lg font-semibold 
                    flex justify-between gap-4
                    {notification.type === 'success' ? 'border-teal-400 text-teal-700' : ''}
                    {notification.type === 'error' ?   'border-red-400 text-red-700' : ''}
                    {notification.type === 'delay' ?   'border-orange-400 text-orange-700' : ''}"
            >
                <div>
                    {notification.message}
                    {#if notification.type == 'delay'}
                        <div class="w-full flex items-center justify-center">
                            <Spinner />
                        </div>
                    {/if}
                </div>
                <button
                    onclick={() => removeNotification(notification)}
                    aria-label="Close notification"
                >
                    &times;
                </button>
            </div>
        {/each}
    </div>
{/key}
