<script>
    import { onMount } from 'svelte';
    import { auth } from '../stores/auth';
    import { login } from '../stores/auth';
    
    let email = '';
    let password = '';
    let error = null;
    let submitting = false;
    let showForm = false;

    function toggleForm() {
        showForm = !showForm;
        if (!showForm) {
            email = '';
            password = '';
            error = null;
        }
    }

    async function handleLogin() {
        if (!email || !password) {
            error = 'Email and password are required';
            return;
        }

        submitting = true;
        error = null;

        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error || 'Invalid credentials');
            }

            const data = await response.json();
            login(data.username);
        } catch (err) {
            error = err.message;
        } finally {
            submitting = false;
        }
    }
</script>

<div class="login-container">
    <button on:click={toggleForm} class="login-toggle">
        {showForm ? 'Login' : 'Login'}
    </button>

    {#if showForm}
        <div class="login-overlay"></div>
        <div class="login-form">
            <div class="login-content">
                {#if error}
                    <div class="error-message">
                        {error}
                    </div>
                {/if}

                <form on:submit|preventDefault={login}>
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input
                            type="email"
                            id="email"
                            bind:value={email}
                            required
                            placeholder="Enter your email"
                        />
                    </div>

                    <div class="form-group">
                        <label for="password">Password</label>
                        <input
                            type="password"
                            id="password"
                            bind:value={password}
                            required
                            placeholder="Enter your password"
                        />
                    </div>

                    <div class="form-actions">
                        <button type="button" on:click={toggleForm} class="cancel-button">
                            Cancel
                        </button>
                        <button type="submit" disabled={submitting}>
                            {submitting ? 'Logging in...' : 'Login'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    {/if}
</div>

<style>
    .login-container {
        position: relative;
        z-index: 1000;
    }

    .login-toggle {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        cursor: pointer;
        font-size: 1rem;
        transition: background-color 0.2s;
    }

    .login-toggle:hover {
        background-color: #45a049;
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

    .login-form {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        padding: 2rem;
        width: 400px;
        max-width: 90%;
        z-index: 1001;
    }

    .login-content {
        max-width: 100%;
    }

    .form-group {
        margin-bottom: 1.5rem;
    }

    label {
        display: block;
        margin-bottom: 0.75rem;
        color: #333;
        font-weight: 500;
    }

    input {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 1rem;
        box-sizing: border-box;
    }

    .form-actions {
        display: flex;
        gap: 1rem;
        margin-top: 1.5rem;
    }

    .cancel-button {
        flex: 1;
        padding: 1rem;
        background-color: #f8f9fa;
        color: #6c757d;
        border: 1px solid #dee2e6;
        border-radius: 4px;
        font-size: 1.1rem;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.2s;
    }

    .cancel-button:hover {
        background-color: #e9ecef;
        border-color: #d1d3d4;
    }

    button[type="submit"] {
        flex: 1;
        padding: 1rem;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        font-size: 1.1rem;
        cursor: pointer;
        font-weight: 500;
        transition: background-color 0.2s;
    }

    button[type="submit"]:hover:not(:disabled) {
        background-color: #45a049;
    }

    button[type="submit"]:disabled {
        background-color: #cccccc;
        cursor: not-allowed;
    }

    .error-message {
        color: #ff4444;
        margin: 1rem 0;
        padding: 0.75rem;
        border-radius: 4px;
        background-color: #ffebee;
        font-size: 0.9rem;
    }
</style>
