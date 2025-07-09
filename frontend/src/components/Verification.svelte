<script>
    import { onMount } from 'svelte';
    
    let listingId = '';
    let thumbsUp = false;
    let comment = '';
    let submitting = false;
    let error = null;

    export let listing;

    $: listingId = listing?.id;

    async function submitVerification() {
        if (!thumbsUp && !comment) {
            error = 'A comment is required for thumbs down verification';
            return;
        }

        submitting = true;
        error = null;

        try {
            const response = await fetch(`/api/businesses/${listingId}/verify`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    thumbs_up: thumbsUp,
                    comment: comment
                })
            });

            if (!response.ok) throw new Error('Failed to submit verification');
        } catch (err) {
            error = err.message;
        } finally {
            submitting = false;
        }
    }
</script>

<div class="verification-container">
    <h3>Verify Listing</h3>

    {#if error}
        <div class="error-message">{error}</div>
    {/if}

    <div class="verification-form">
        <div class="verification-options">
            <label>
                <input
                    type="radio"
                    bind:group={thumbsUp}
                    value={true}
                />
                Thumbs Up (Verified)
            </label>
            <label>
                <input
                    type="radio"
                    bind:group={thumbsUp}
                    value={false}
                />
                Thumbs Down (Not Verified)
            </label>
        </div>

        {#if !thumbsUp}
            <div class="comment-section">
                <label for="comment">Comment (required for thumbs down):</label>
                <textarea
                    id="comment"
                    bind:value={comment}
                    rows="3"
                    placeholder="Please explain why this listing is inaccurate..."
                ></textarea>
            </div>
        {/if}

        <button on:click={submitVerification} disabled={submitting}>
            {submitting ? 'Submitting...' : 'Submit Verification'}
        </button>
    </div>
</div>

<style>
    .verification-container {
        margin: 2rem 0;
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 4px;
        background-color: white;
    }

    .verification-options {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .comment-section {
        margin-top: 1rem;
    }

    textarea {
        width: 100%;
        padding: 0.5rem;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    button {
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }

    button:disabled {
        background-color: #cccccc;
        cursor: not-allowed;
    }

    .error-message {
        color: red;
        margin: 1rem 0;
    }
</style>
