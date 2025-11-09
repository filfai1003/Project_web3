<script lang="ts">
  import { onMount } from 'svelte';
  import '../style/header.css';
  import { loggedIn, logout, profile, restoreProfileFromCookie } from '../stores/authStore';
  export let title: string = 'Project Web3';

  onMount(() => {
    try { restoreProfileFromCookie(); } catch (e) {}
  });
</script>

<header class="app-header">
  <div class="brand"><a href="/">{title}</a></div>
  <nav class="nav">
    <a href="/">Home</a>
    <a href="/games">Games</a>
    {#if $loggedIn}
      <span class="who">{ $profile?.username ?? 'User' }</span>
      <button class="logout" on:click={logout}>Logout</button>
    {:else}
      <a href="/oauth">Login</a>
    {/if}
  </nav>
</header>

