<script>
    import BusinessForm from '../components/BusinessForm.svelte';
    import Verification from '../components/Verification.svelte';
    import { auth } from '../stores/auth.js';

    let listing = {
        business_name: '',
        street1: '',
        street2: '',
        city: '',
        state: '',
        zip_code: '',
        phone: '',
        business_type: '',
        fulltime_min_age: 14,
        parttime_min_age: 14
    };
</script>

<div class="business-listings-page">
    <h1>Business Listings</h1>
    
    {#if $auth.isAuthenticated}
        <BusinessForm {listing} />
        <Verification />
    {/if}
</div>

<style>
    .business-listings-page {
        padding: 2rem 0;
    }
    h1 {
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
