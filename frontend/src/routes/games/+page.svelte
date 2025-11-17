<script lang="ts">
  import "../../style/games.css";
  import type { Game } from "../../api/games";
  import {
    fetchGames,
    fetchGamesByOwner,
    deleteGameById,
  } from "../../api/games";
  import { getCookie } from "../../utils/cookies";
  import { onMount } from "svelte";

  let loadingAll = true;
  let loadingMine = false;
  let errorAll: string | null = null;
  let errorMine: string | null = null;

  let communityGames: Game[] = [];
  let personalGames: Game[] = [];

  let hasAuth = false;

  onMount(() => {
    setInitialView();
    void loadCommunity();
    void loadPersonal();
  });

  function setInitialView() {
    try {
      const params = new URLSearchParams(window.location.search);
      if (params.get("view") === "mine") {
        document
          .getElementById("personal-section")
          ?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    } catch (e) {}
  }

  async function loadCommunity() {
    errorAll = null;
    try {
      communityGames = await fetchGames();
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      errorAll = message || "Unable to load games right now.";
    } finally {
      loadingAll = false;
    }
  }

  async function loadPersonal() {
    errorMine = null;
    try {
      const ownerId = getCookie("user_id");
      hasAuth = Boolean(ownerId);
      if (!hasAuth || !ownerId) {
        personalGames = [];
        return;
      }
      loadingMine = true;
      personalGames = await fetchGamesByOwner(ownerId);
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      errorMine = message || "Unable to load your games.";
    } finally {
      loadingMine = false;
    }
  }

  async function deleteGame(gameId: string) {
    errorMine = null;
    try {
      const ownerId = getCookie('user_id');
      if (!ownerId) {
        throw new Error('Authentication required');
      }
      await deleteGameById(gameId);
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      errorMine = message || "Unable to delete the game.";
    }
    loadPersonal();
    loadCommunity();
  }
</script>

<section class="games-shell">
  <header class="games-header">
    <div>
      <h1>Your adventure hub</h1>
      <p>Pick up your stories or dive into fresh community-made quests.</p>
    </div>
    <a class="create" href="/games/new">Start a new adventure</a>
  </header>

  <div class="games-sections">
    <section id="personal-section" class="games-section">
      <div class="section-header">
        <h2>My library</h2>
      </div>

      {#if !hasAuth}
        <div class="state">Log in to see and manage your games.</div>
      {:else if loadingMine}
        <div class="state">Fetching your library...</div>
      {:else if errorMine}
        <div class="state error">{errorMine}</div>
      {:else if personalGames.length === 0}
        <div class="state">No games yet. Kick off a new adventure.</div>
      {:else}
        <div class="games-grid">
          {#each personalGames as game (game.game_id)}
            <div class="game-card-wrapper">
              <button
                class="delete-btn"
                on:click={() => deleteGame(game.game_id)}
                aria-label="Delete game"
              >
                Delete
              </button>
              <a class="game-card" href={`/games/${game.game_id}`}>
                <div class="card-title">{game.title}</div>
                <div class="card-meta">
                  <span>{game.interactions.length} interactions</span>
                  <span class="hint">Continue adventure</span>
                </div>
              </a>
            </div>
          {/each}
        </div>
      {/if}
    </section>

    <section class="games-section">
      <div class="section-header">
        <h2>Community spotlight</h2>
        <span class="section-note">Updated in real time</span>
      </div>

      {#if loadingAll}
        <div class="state">Loading games...</div>
      {:else if errorAll}
        <div class="state error">{errorAll}</div>
      {:else if communityGames.length === 0}
        <div class="state">
          No games available yet. Be the first to create one!
        </div>
      {:else}
        <div class="games-grid">
          {#each communityGames as game (game.game_id)}
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
  </div>
</section>
