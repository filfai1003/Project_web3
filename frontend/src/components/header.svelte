<script lang="ts">
  import { onMount } from 'svelte';
  import '../style/header.css';
  import { loggedIn, logout, profile, restoreProfileFromCookie } from '../stores/authStore';
  import type { UserProfile } from '../stores/authStore';

  export let title: string = 'Project Web3';
  export let initialAuth: { loggedIn?: boolean; profile?: UserProfile | null } | null = null;

  let displayLoggedIn: boolean | undefined = initialAuth?.loggedIn;
  let displayProfile: UserProfile | null | undefined = initialAuth?.profile;

  $: displayLoggedIn = initialAuth?.loggedIn ?? $loggedIn;
  $: displayProfile = initialAuth?.profile ?? $profile;

  onMount(() => {
    try { restoreProfileFromCookie(); } catch (e) {}
  });
</script>

<header class="app-header">
  <div class="brand"><a href="/">{title}</a></div>
  <nav class="nav">
    <a href="/">Home</a>
    <a href="/games">Games</a>
    {#if displayLoggedIn}
      <a href="/games/mine">My Games</a>
      <span class="who">{ displayProfile?.username ?? 'User' }</span>
      <button class="logout" on:click={logout}>Logout</button>
    {:else}
      <a href="/oauth">Login</a>
    {/if}
  </nav>
</header>

