<script>
    import { onMount } from 'svelte';
    
    export let listing = {}; // Optional prop with default empty object
    
    let business_name = '';
    let street1 = '';
    let street2 = '';
    let city = '';
    let state = '';
    let zip_code = '';
    let phone = '';
    let business_type = '';
    let fulltime_min_age = 14;
    let parttime_min_age = 14;
    let error = null;
    let submitting = false;

    const businessTypes = [
        'entertainment',
        'food',
        'sports',
        'apparel',
        'retail',
        'electronics',
        'other'
    ];

    async function submitListing() {
        submitting = true;
        error = null;
        
        try {
            const response = await fetch('/api/businesses', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    business_name,
                    street1,
                    street2,
                    city,
                    state,
                    zip_code,
                    phone,
                    business_type,
                    fulltime_min_age,
                    parttime_min_age
                })
            });
            
            if (!response.ok) throw new Error('Failed to submit listing');
            
            // Clear form after successful submission
            business_name = '';
            street1 = '';
            street2 = '';
            city = '';
            state = '';
            zip_code = '';
            phone = '';
            business_type = '';
            fulltime_min_age = 14;
            parttime_min_age = 14;
        } catch (err) {
            error = err.message;
        } finally {
            submitting = false;
        }
    }
</script>

<div class="form-container">
    <h2>Add New Business Listing</h2>
    
    {#if error}
        <div class="error-message">{error}</div>
    {/if}

    <form on:submit|preventDefault={submitListing}>
        <div class="form-group">
            <label for="business_name">Business Name</label>
            <input
                type="text"
                id="business_name"
                bind:value={business_name}
                required
            />
        </div>

        <div class="form-group">
            <label for="street1">Street Address 1</label>
            <input
                type="text"
                id="street1"
                bind:value={street1}
                required
            />
        </div>

        <div class="form-group">
            <label for="street2">Street Address 2</label>
            <input
                type="text"
                id="street2"
                bind:value={street2}
            />
        </div>

        <div class="form-group">
            <label for="city">City</label>
            <input
                type="text"
                id="city"
                bind:value={city}
                required
            />
        </div>

        <div class="form-group">
            <label for="state">State</label>
            <input
                type="text"
                id="state"
                bind:value={state}
                maxlength="2"
                required
            />
        </div>

        <div class="form-group">
            <label for="zip_code">Zip Code</label>
            <input
                type="text"
                id="zip_code"
                bind:value={zip_code}
                required
            />
        </div>

        <div class="form-group">
            <label for="phone">Phone</label>
            <input
                type="tel"
                id="phone"
                bind:value={phone}
            />
        </div>

        <div class="form-group">
            <label for="business_type">Business Type</label>
            <select
                id="business_type"
                bind:value={business_type}
                required
            >
                {#each businessTypes as type}
                    <option value={type}>{type}</option>
                {/each}
            </select>
        </div>

        <div class="age-group">
            <div class="form-group">
                <label for="fulltime_min_age">Full-time Min Age</label>
                <select
                    id="fulltime_min_age"
                    bind:value={fulltime_min_age}
                    required
                >
                    <option value="14">14</option>
                    <option value="15">15</option>
                    <option value="16">16</option>
                    <option value="17">17</option>
                    <option value="18">18</option>
                </select>
            </div>

            <div class="form-group">
                <label for="parttime_min_age">Part-time Min Age</label>
                <select
                    id="parttime_min_age"
                    bind:value={parttime_min_age}
                    required
                >
                    <option value="14">14</option>
                    <option value="15">15</option>
                    <option value="16">16</option>
                    <option value="17">17</option>
                    <option value="18">18</option>
                </select>
            </div>
        </div>

        <button type="submit" disabled={submitting}>
            {submitting ? 'Submitting...' : 'Submit Listing'}
        </button>
    </form>
</div>

<style>
    .form-container {
        max-width: 600px;
        margin: 2rem auto;
        padding: 2rem;
    }

    .form-group {
        margin-bottom: 1rem;
    }

    label {
        display: block;
        margin-bottom: 0.5rem;
    }

    input, select {
        width: 100%;
        padding: 0.5rem;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    .age-group {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
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
