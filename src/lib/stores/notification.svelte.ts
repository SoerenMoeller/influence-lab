type Notification = {
    id: number;
    message: string;
    type?: 'success' | 'error' | 'delay';
    duration?: number;
};

export const notifications: Notification[] = $state([]);
let count = 0;

export function showNotification(message: string, type: Notification["type"], duration = 8000): Notification {
    const id = count++;
    const notification = {
        id, message, type, duration
    };
    notifications.push(notification);

    if (type == 'delay') return notification;

    setTimeout(() => {
        removeNotification(notification);
    }, duration);
    
    return notification;
}

export function removeNotification(notification: Notification) {
    const index = notifications.findIndex(n => n.id === notification.id);
    if (index == -1) return;
    notifications.splice(index, 1);
}
