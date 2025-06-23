import { writable } from 'svelte/store';

type Notification = {
    id: number;
    message: string;
    type?: 'success' | 'error';
    duration?: number;
};

const toasts = writable<Notification[]>([]);

let counter = 0;

export function showNotification(message: string, type: Notification["type"], duration = 8000) {
    const id = counter++;
    toasts.update((all) => [...all, { id, message, type, duration }]);

    setTimeout(() => {
        toasts.update((all) => all.filter((t) => t.id !== id));
    }, duration);
}

export function removeNotification(id: number) {
    toasts.update((all) => all.filter((t) => t.id !== id));
}

export default toasts;
