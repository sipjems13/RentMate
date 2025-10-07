import { apiRegister, apiLogin } from './api.js';
import { supabaseSignUp } from './supabase.js';

async function handleRegister(event) {
    event.preventDefault();

    const getVal = (id) => (document.getElementById(id)?.value || '');

    const email = getVal('reg-email');
    const password = getVal('reg-password');
    const confirmPassword = getVal('confirm-password');
    const firstName = getVal('first-name');
    const lastName = getVal('last-name');
    const address = getVal('address');
    const phone = getVal('phone');
    const city = getVal('city');
    const state = getVal('state');
    const role = (document.getElementById('role')?.value || 'tenant');

    if (password !== confirmPassword) {
        alert('Passwords do not match.');
        return;
    }

    try {
        const payload = { email, password, role, firstName, lastName, address, phone, city, state };
        if (role === 'landlord') {
            // Use Supabase Auth for landlord self-signup
            await supabaseSignUp(payload);
        } else {
            // For tenants, still go through backend so landlord-only rule applies
            await apiRegister(payload);
        }
        alert('Registration successful! Please login.');
        window.location.href = role === 'landlord' ? '/landlord-login/' : '/tenant-login/';
    } catch (error) {
        alert(`Registration failed: ${error.message}`);
    }
}

async function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        // Try backend login first (for tenants created by landlord via backend)
        try {
            const { access_token } = await apiLogin({ email, password });
            localStorage.setItem('rentmate_token', access_token);
            alert('Login successful! Redirecting to dashboard...');
            window.location.href = '/dashboard/';
            return;
        } catch (_) {}

        // Fallback to Supabase Auth (for landlords and any user in Supabase Auth)
        await supabaseSignIn(email, password);
        alert('Login successful! Redirecting to dashboard...');
        window.location.href = '/dashboard/';
    } catch (error) {
        alert(`Login failed: ${error.message}`);
    }
}

window.handleRegister = handleRegister;
window.handleLogin = handleLogin;
