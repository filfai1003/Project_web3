<script lang="ts">
  import '../../../style/games.css';
  import GameCard from '../../../components/game_card.svelte';
  import { fetchGameById } from '../../../api/games';
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { playerPlay, narratorPlay } from '../../../api/play';
  import { getCookie } from '../../../utils/cookies';

  let game: any = null;
  let loading = true;
  let error: string | null = null;
  let inputText: string = '';
  let submitting: boolean = false;

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

  async function submitInteraction() {
    submitting = true;
    error = null;
    try {
      const token = getCookie('token');
      if (!token) { window.location.href = '/oauth'; return; }

      if (!inputText || inputText.trim() === '') {
        // request narrator
        const text = await narratorPlay(String(gameId), token);
        // backend streaming response may include appended JSON; try to split
        let content = text;
        const marker = '\n__INTERACTION_JSON__\n';
        if (content.includes(marker)) {
          content = content.split(marker)[0];
        }
        const interaction = {
          interaction_id: 'local-' + Date.now(),
          sender: 'assistant',
          content: String(content).trim(),
          created_at: new Date().toISOString()
        };
        game.interactions = game.interactions || [];
        game.interactions.push(interaction);
      } else {
        // send player message
        const out = await playerPlay(String(gameId), inputText, token);
        game.interactions = game.interactions || [];
        game.interactions.push(out);
        inputText = '';
      }
    } catch (e) {
      error = (e as Error)?.message ?? String(e);
    } finally {
      submitting = false;
    }
  }
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
        <div style="margin:0.75rem 0">
          <textarea placeholder="Type an action, or leave empty to call the narrator" bind:value={inputText} rows="3" style="width:100%; padding:0.5rem; border-radius:6px; background:var(--surface); color:inherit; border:1px solid rgba(255,255,255,0.03);"></textarea>
          <div style="display:flex; gap:0.5rem; margin-top:0.5rem; align-items:center;">
            <button class="create-btn" on:click={submitInteraction} disabled={submitting}>{submitting ? 'Sending...' : 'Send'}</button>
            <div class="muted">Leave empty to request narrator turn</div>
          </div>
          {#if error}
            <p class="muted">Error: {error}</p>
          {/if}
        </div>
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
