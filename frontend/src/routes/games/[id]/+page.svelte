<script lang="ts">
  import '../../../style/games.css';
  import GameCard from '../../../components/game_card.svelte';
  import { fetchGameById } from '../../../api/games';
  import { onMount } from 'svelte';
  import { page } from '$app/stores';

  let game: any = null;
  let loading = true;
  let error: string | null = null;

  $: gameId = $page.params.id;

  onMount(async () => {
    loading = true;
    error = null;
    try {
      game = await fetchGameById(String(gameId));
    } catch (e) {
      error = (e as Error)?.message ?? String(e);
    } finally {
      loading = false;
    }
  });
</script>

<div class="games-container">
  {#if loading}
    <p class="loader">Loading game...</p>
  {:else if error}
    <p class="muted">Error: {error}</p>
  {:else if !game}
    <p class="muted">Game not found.</p>
  {:else}
    <div class="center">
      <h1>{game.title}</h1>
      <GameCard {game} />
      <section>
        <h2>Interactions</h2>
        {#if game.interactions?.length}
          <ul>
            {#each game.interactions as it}
              <li class="muted">{it.sender}: {it.content}</li>
            {/each}
          </ul>
        {:else}
          <p class="muted">No interactions yet.</p>
        {/if}
      </section>
    </div>
  {/if}
</div>
