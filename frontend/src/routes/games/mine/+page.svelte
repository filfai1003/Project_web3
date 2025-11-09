<script lang="ts">
  import { onMount } from 'svelte';
  import '../../../style/games.css';
  import GameCard from '../../../components/game_card.svelte';
  import type { Game } from '../../../api/games';
  import { fetchGamesByOwner } from '../../../api/games';
  import { profile } from '../../../stores/authStore';
  import { get } from 'svelte/store';
  import { getCookie } from '../../../utils/cookies';

  let games: Game[] = [];
  let loading = true;
  let error: string | null = null;

  function createNew() {
    const token = getCookie('token');
    if (!token) { window.location.href = '/oauth'; return; }
    window.location.href = '/games/new';
  }

  onMount(async () => {
    loading = true;
    error = null;
    const p = get(profile);
    const owner_id = p?.user_id;
    if (!owner_id) {
      error = 'You must be logged in to view your games.';
      loading = false;
      return;
    }

    try {
      const token = getCookie('token') ?? undefined;
      games = await fetchGamesByOwner(String(owner_id), token);
    } catch (e) {
      error = (e as Error)?.message ?? String(e);
    } finally {
      loading = false;
    }
  });
</script>

<div class="games-container">
  <div class="grid-header">
    <h1>My games</h1>
    <div class="muted">{games.length} games</div>
    <button class="create-btn" on:click={createNew}>Create new</button>
  </div>

  {#if loading}
    <p class="loader">Loading your games...</p>
  {:else if error}
    <p class="muted">Error: {error}</p>
  {:else if games.length === 0}
    <p class="muted">You have no games yet.</p>
  {:else}
    <div class="game-list">
      {#each games as g}
        <GameCard game={g} />
      {/each}
    </div>
  {/if}
</div>
