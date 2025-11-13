<script lang="ts">
  import { onMount } from 'svelte';
  import '../style/header.css';
  import { loggedIn, logout, profile, restoreProfileFromCookie } from '../stores/authStore';
  import type { UserProfile } from '../stores/authStore';

  export let title: string = 'Project Web3';
  export let initialAuth: { loggedIn?: boolean; profile?: UserProfile | null } | null = null;

  let menuOpen = false;
  let displayLoggedIn: boolean | undefined = initialAuth?.loggedIn;
  let displayProfile: UserProfile | null | undefined = initialAuth?.profile;
  let usingInitial = true;

  const links = [
    { href: '/', label: 'Home', auth: false },
    { href: '/games', label: 'Games', auth: false },
  ];

  $: displayLoggedIn = usingInitial && initialAuth?.loggedIn !== undefined ? initialAuth.loggedIn : $loggedIn;
  $: displayProfile = usingInitial && initialAuth?.profile !== undefined ? initialAuth.profile : $profile;

  onMount(() => {
    usingInitial = false;
    try { restoreProfileFromCookie(); } catch (e) {}
  });

  function toggleMenu() {
    menuOpen = !menuOpen;
  }

  function closeMenu() {
    menuOpen = false;
  }

  function handleLogout() {
    closeMenu();
    logout();
  }

  function initials() {
    const name = displayProfile?.username ?? displayProfile?.email ?? '';
    return name ? name.slice(0, 2).toUpperCase() : 'ME';
  }
</script>

<header class="app-header">
  <div class="header-inner">
    <a class="brand" href="/" on:click={closeMenu}>{title}</a>
    <button class="menu-toggle" aria-label="Toggle menu" aria-expanded={menuOpen} on:click={toggleMenu}>
      <span></span>
      <span></span>
      <span></span>
    </button>
    <nav class:open={menuOpen}>
      {#each links as link (link.href)}
        {#if !link.auth || displayLoggedIn}
          <a href={link.href} on:click={closeMenu}>{link.label}</a>
        {/if}
      {/each}
      {#if displayLoggedIn}
  <div class="profile">
          <span class="avatar">{initials()}</span>
          <div class="details">
            <strong>{displayProfile?.username ?? 'Player'}</strong>
            {#if displayProfile?.email}
              <small>{displayProfile.email}</small>
            {/if}
          </div>
        </div>
        <button class="logout" type="button" on:click={handleLogout}>Logout</button>
      {:else}
        <a class="cta" href="/oauth" on:click={closeMenu}>Login</a>
      {/if}
    </nav>
  </div>
</header>

