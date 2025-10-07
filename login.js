// Show that the newest version of the file is loaded
console.log('Loaded updated login.js v2 — cache busting active:', new Date().toISOString());

// Clear old cached versions so the browser always loads the latest
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistrations().then(registrations => {
        for (let registration of registrations) registration.unregister();
    });
    caches.keys().then(names => {
        for (let name of names) caches.delete(name);
    });
}

import { apiLogin } from './api.js';
import { supabaseSignIn } from './supabase.js';

async function handleLogin(event) {
    event.preventDefault();

    const emailEl = document.getElementById('login-email') || document.getElementById('email');
    const passEl = document.getElementById('login-password') || document.getElementById('password');
    const email = emailEl ? emailEl.value : '';
    const password = passEl ? passEl.value : '';

    try {
        // Try backend login first
        try {
            const { access_token } = await apiLogin({ email, password });
            localStorage.setItem('rentmate_token', access_token);
            alert('Login successful! Redirecting to dashboard...');
            window.location.href = '/dashboard/';  
            return;
        } catch (_) {}

        // Fallback to Supabase Auth
        await supabaseSignIn(email, password);
        alert('Login successful! Redirecting to dashboard...');
        window.location.href = '/dashboard/';   
    } catch (error) {
        alert('Login failed: ' + (error?.message || 'Unknown error'));
    }
}

document.getElementById('loginForm').addEventListener('submit', handleLogin);
