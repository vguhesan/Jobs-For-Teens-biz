<script>
    import { onMount } from 'svelte';
    
    let city = '';
    let state = '';
    let zip = '';
    let minAge = 14;
    let results = [];
    let loading = false;
    let error = null;

    async function search() {
        loading = true;
        error = null;
        try {
            const response = await fetch(`/api/businesses?city=${city}&state=${state}&zip=${zip}&min_age=${minAge}`);
            if (!response.ok) throw new Error('Search failed');
            results = await response.json();
        } catch (err) {
            error = err.message;
        } finally {
            loading = false;
        }
    }
</script>

<div class="search-container">
    <h1 class="search-title">Find Local Jobs for Teens</h1>
    <div class="search-form">
        <input
            bind:value={city}
            placeholder="City"
            class="search-input"
        />
        <input
            bind:value={state}
            placeholder="State"
            class="search-input"
            maxlength="2"
        />
        <input
            bind:value={zip}
            placeholder="Zip Code"
            class="search-input"
        />
        <select bind:value={minAge} class="search-input">
            <option value="14">14</option>
            <option value="15">15</option>
            <option value="16">16</option>
            <option value="17">17</option>
            <option value="18">18</option>
        </select>
        <button on:click={search} class="search-button">
            {loading ? 'Searching...' : 'Search'}
        </button>
    </div>

    {#if error}
        <div class="error-message">{error}</div>
    {/if}

    {#if results.length > 0}
        <div class="results">
            {#each results as listing}
                <div class="listing-card">
                    <h2>{listing.business_name}</h2>
                    <p><strong>Address:</strong> {listing.address}</p>
                    <p><strong>Phone:</strong> {listing.phone}</p>
                    <p><strong>Type:</strong> {listing.business_type}</p>
                    <p><strong>Full-time Min Age:</strong> {listing.fulltime_min_age}</p>
                    <p><strong>Part-time Min Age:</strong> {listing.parttime_min_age}</p>
                    <p><strong>Verified:</strong> {listing.verified ? 'Yes' : 'No'}</p>
                </div>
            {/each}
        </div>
    {/if}
</div>

<style>
    .search-title {
        font-size: 1.5rem;
        margin-bottom: 2rem;
    }

    .search-container {
        max-width: 800px;
        margin: 2rem auto;
        padding: 2rem;
    }

    .search-form {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
    }

    .search-input {
        flex: 1;
        padding: 0.5rem;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    .search-button {
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }

    .search-button:hover {
        background-color: #45a049;
    }

    .error-message {
        color: red;
        margin: 1rem 0;
    }

    .results {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1rem;
    }

    .listing-card {
        border: 1px solid #ddd;
        padding: 1rem;
        border-radius: 4px;
        background-color: white;
    }
</style>
