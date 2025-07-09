<script>
    import { onMount } from 'svelte';
    
    let username = '';
    let email = '';
    let password = '';
    let confirmPassword = '';
    let error = null;
    let submitting = false;
    let onCancel;

    export let onFormCancel;

    function handleCancel() {
        if (onFormCancel) {
            onFormCancel();
        }
    }

    async function register() {
        if (password !== confirmPassword) {
            error = 'Passwords do not match';
            return;
        }

        if (!username || !email || !password) {
            error = 'All fields are required';
            return;
        }

        submitting = true;
        error = null;

        try {
            const response = await fetch('/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username,
                    email,
                    password
                })
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error || 'Registration failed');
            }

            // Clear form after successful registration
            username = '';
            email = '';
            password = '';
            confirmPassword = '';
            
            // Show success message
            error = 'Registration successful! Please log in.';
        } catch (err) {
            error = err.message;
        } finally {
            submitting = false;
        }
    }
</script>

<div class="registration-container">
    <h2>Register</h2>

    {#if error}
        <div class="error-message">
            {error}
        </div>
    {/if}

    <form on:submit|preventDefault={register}>
        <div class="form-group">
            <label for="username">Username</label>
            <input
                type="text"
                id="username"
                bind:value={username}
                required
            />
        </div>

        <div class="form-group">
            <label for="email">Email</label>
            <input
                type="email"
                id="email"
                bind:value={email}
                required
            />
        </div>

        <div class="form-group">
            <label for="password">Password</label>
            <input
                type="password"
                id="password"
                bind:value={password}
                required
            />
        </div>

        <div class="form-group">
            <label for="confirmPassword">Confirm Password</label>
            <input
                type="password"
                id="confirmPassword"
                bind:value={confirmPassword}
                required
            />
        </div>

        <div class="form-actions">
            <button type="button" on:click={handleCancel} class="cancel-button">
                Cancel
            </button>
            <button type="submit" disabled={submitting}>
                {submitting ? 'Registering...' : 'Register'}
            </button>
        </div>
    </form>
</div>

<style>
    .registration-container {
        max-width: 400px;
        width: 80%;
        margin: 2rem auto;
        padding: 2rem;
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
        padding: 0.75rem;
        background-color: #f8f9fa;
        color: #6c757d;
        border: 1px solid #dee2e6;
        border-radius: 4px;
        font-size: 1rem;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.2s;
    }

    .cancel-button:hover {
        background-color: #e9ecef;
        border-color: #d1d3d4;
    }

    button {
        flex: 1;
        padding: 0.75rem;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        font-size: 1rem;
        cursor: pointer;
    }

    button:disabled {
        background-color: #cccccc;
        cursor: not-allowed;
    }

    .error-message {
        color: #ff4444;
        margin: 1rem 0;
        padding: 0.5rem;
        border-radius: 4px;
        background-color: #ffebee;
    }
</style>
