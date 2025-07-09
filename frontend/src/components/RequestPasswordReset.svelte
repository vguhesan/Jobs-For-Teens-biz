<script>
    import { onMount } from 'svelte';
    
    let email = '';
    let error = null;
    let success = null;
    let submitting = false;
    let onCancel;

    export let onFormCancel;

    function handleCancel() {
        if (onFormCancel) {
            onFormCancel();
        }
    }

    async function requestReset() {
        if (!email) {
            error = 'Email is required';
            return;
        }

        submitting = true;
        error = null;
        success = null;

        try {
            const response = await fetch('/api/reset-password/request', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email })
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error || 'Failed to request password reset');
            }

            success = 'If an account exists with this email, you will receive a password reset link.';
            email = '';
        } catch (err) {
            error = err.message;
        } finally {
            submitting = false;
        }
    }
</script>

<div class="reset-container">
    <h2>Forgot Password?</h2>

    {#if success}
        <div class="success-message">
            {success}
        </div>
    {/if}

    {#if error}
        <div class="error-message">
            {error}
        </div>
    {/if}

    <form on:submit|preventDefault={requestReset}>
        <div class="form-group">
            <label for="email">Email</label>
            <input
                type="email"
                id="email"
                bind:value={email}
                required
                placeholder="Enter your email address"
            />
        </div>

        <div class="form-actions">
            <button type="button" on:click={handleCancel} class="cancel-button">
                Cancel
            </button>
            <button type="submit" disabled={submitting}>
                {submitting ? 'Sending...' : 'Send Reset Link'}
            </button>
        </div>
    </form>
</div>

<style>
    .reset-container {
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

    .success-message {
        color: #4CAF50;
        margin: 1rem 0;
        padding: 0.5rem;
        border-radius: 4px;
        background-color: #e8f5e9;
    }
</style>
