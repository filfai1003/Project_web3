<script lang="ts">
  import '../../../style/gamesnew.css';
  import { createGame } from '../../../api/games';
  import { getCookie } from '../../../utils/cookies';

  let title = '';
  let loading = false;
  let error: string | null = null;

  async function submit() {
    error = null;
    loading = true;
    try {
      const token = getCookie('token');
      if (!token) {
        window.location.href = '/oauth';
        return;
      }

      const g = await createGame(title, token);
      try { window.location.href = '/games/' + g.game_id; } catch (e) { window.location.href = '/games'; }
    } catch (e) {
      error = (e as Error)?.message ?? String(e);
    } finally { loading = false; }
  }
</script>

<div class="games-container">
  <div class="grid-header">
    <h1>Create game</h1>
  </div>

  <form on:submit|preventDefault={submit}>
    <div class="field">
      <label>Title
        <input type="text" bind:value={title} placeholder="My new adventure" required />
      </label>
    </div>

    <div style="margin-top:0.75rem;">
      <button class="create-btn" disabled={loading}>{loading ? 'Creating...' : 'Create game'}</button>
    </div>

    {#if error}
      <p class="muted" style="margin-top:0.5rem;color:#ff8b8b;">{error}</p>
    {/if}
  </form>
</div>
