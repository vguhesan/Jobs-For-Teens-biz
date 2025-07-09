import { writable } from 'svelte/store';

export const auth = writable({
    isAuthenticated: false,
    username: ''
});

export function login(username) {
    auth.set({
        isAuthenticated: true,
        username
    });
}

export function logout() {
    auth.set({
        isAuthenticated: false,
        username: ''
    });
}
