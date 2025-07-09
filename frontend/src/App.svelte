<script>
    import Search from './components/Search.svelte';
    import BusinessForm from './components/BusinessForm.svelte';
    import Verification from './components/Verification.svelte';
    import Registration from './components/Registration.svelte';
    import { auth, logout } from './stores/auth.js';
    import RequestPasswordReset from './components/RequestPasswordReset.svelte';
    import ResetPassword from './components/ResetPassword.svelte';
    import Login from './components/Login.svelte';
    import { onMount } from 'svelte';
    import logo from './assets/j4t-logo.svg';

    let showRegistration = false;
    let showPasswordReset = false;
    let resetToken = '';
    let username = '';

    auth.subscribe(value => {
        username = value.username;
    });

    function handleLogout() {
        logout();
    }


    function toggleRegistration() {
        showRegistration = !showRegistration;
        showPasswordReset = false;
    }

    function togglePasswordReset() {
        showPasswordReset = !showPasswordReset;
        showRegistration = false;
    }

    // Handle password reset URL parameter
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    if (token) {
        resetToken = token;
        showPasswordReset = true;
    }    
</script>

<div class="app-container">
    <nav>
            <div class="nav-content">
                <div class="nav-brand">
                    <a class="navbar-brand" href="/"><img src={logo} alt="Jobs for Teens" id="logo" width="350"/></a>
                </div>
                <div class="auth-buttons">
                    {#if $auth.isAuthenticated}
                        <a href="/business-listings" class="nav-button">Business Listings</a>
                        <button on:click={handleLogout}>
                            Logout ({username})
                        </button>
                    {:else}
                        <Login />
                        <button on:click={toggleRegistration}>
                            Register
                        </button>
                        <button on:click={togglePasswordReset}>
                            Forgot Password
                        </button>
                    {/if}
                </div>
            </div>
    </nav>

    <div class="main-content">
        {#if !showRegistration && !showPasswordReset}
            <Search />
        {/if}

        {#if showRegistration}
            <Registration onFormCancel={() => {
                showRegistration = false;
                showPasswordReset = false;
            }} />
        {/if}

        {#if showPasswordReset}
            {#if resetToken}
                <ResetPassword resetToken={resetToken} onFormCancel={() => {
                    showPasswordReset = false;
                    showRegistration = false;
                }} />
            {:else}
                <RequestPasswordReset onFormCancel={() => showPasswordReset = false} />
            {/if}
        {/if}
    </div>
</div>

<style>
    .app-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 1rem;
        width: 800px;
    }

    nav {
        background-color: white;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        position: relative;
        width: 100%;
    }

    .nav-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
        width: 100%;
    }

    .nav-brand {
        width: 200px;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .home-button {
        background: none;
        border: none;
        cursor: pointer;
        padding: 0;
        transition: transform 0.2s;
    }

    .home-button:hover {
        transform: scale(1.1);
    }

    .home-button svg {
        fill: #4CAF50;
    }

    .home-button:hover svg {
        fill: #45a049;
    }

    h1 {
        margin: 0;
        font-size: 1.5rem;
    }

    .auth-buttons {
        display: flex;
        gap: 1rem;
        align-items: center;
    }

    .login-form {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 1001;
    }

    .login-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 1000;
    }

    .main-content {
        margin-top: 2rem;
        align-items: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 8px;
    }

    h1 {
        margin: 0;
        font-size: 2rem;
    }

    .auth-buttons {
        display: flex;
        gap: 1rem;
    }

    nav button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        cursor: pointer;
        font-size: 1rem;
    }

    nav button:hover {
        background-color: #45a049;
    }

    .main-content {
        display: grid;
        gap: 2rem;
    }
</style>
