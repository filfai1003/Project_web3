<script lang="ts">
  import '../../style/games.css';
  import type { Game } from '../../api/games';
  import { fetchGames } from '../../api/games';
  import { onMount } from 'svelte';

  let loading = true;
  let error: string | null = null;
  let games: Game[] = [];

  onMount(() => {
    (async () => {
      try {
        games = await fetchGames();
      } catch (err) {
        const message = err instanceof Error ? err.message : String(err);
        error = message || 'Unable to load games right now.';
      } finally {
        loading = false;
      }
    })();
  });
</script>

<section class="games-shell">
  <header class="games-header">
    <div>
      <h1>Discover games</h1>
      <p>Breeze through the latest adventures created by the community.</p>
    </div>
    <a class="create" href="/games/new">Create a game</a>
  </header>

  {#if loading}
    <div class="state">Loading games...</div>
  {:else if error}
    <div class="state error">{error}</div>
  {:else if games.length === 0}
    <div class="state">No games available yet. Be the first to create one!</div>
  {:else}
    <div class="games-grid">
      {#each games as game (game.game_id)}
        <a class="game-card" href={`/games/${game.game_id}`}>
          <div class="card-title">{game.title}</div>
          <div class="card-meta">
            <span>{game.interactions.length} interactions</span>
            <span>Owner #{game.owner_id.slice(0, 6)}</span>
          </div>
        </a>
      {/each}
    </div>
  {/if}
</section>
