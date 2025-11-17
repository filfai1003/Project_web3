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
        const hasAuth = !!getCookie('username') || !!getCookie('user_id');
        if (!hasAuth) {
          window.location.href = '/oauth';
          return;
        }

        const g = await createGame(title);
      try { window.location.href = '/games/' + g.game_id; } catch (e) { window.location.href = '/games'; }
    } catch (e) {
      error = (e as Error)?.message ?? String(e);
    } finally { loading = false; }
  }
</script>

<div class="games-new-shell">
  <header class="games-new-header">
    <h1>Create a new game</h1>
    <p>Give your quest a memorable title to keep it easy to find later.</p>
  </header>

  <form class="games-new-form" on:submit|preventDefault={submit}>
    <label class="field">
      <span>Title</span>
      <input type="text" bind:value={title} placeholder="My new adventure" required />
    </label>

    {#if error}
      <p class="form-error">{error}</p>
    {/if}

    <button class="create-btn" type="submit" disabled={loading}>
      {#if loading}
        Creating...
      {:else}
        Create game
      {/if}
    </button>
  </form>
</div>
