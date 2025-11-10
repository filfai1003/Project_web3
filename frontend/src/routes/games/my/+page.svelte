<script lang="ts">
	import '../../../style/gamesmy.css';
	import type { Game } from '../../../api/games';
	import { fetchGamesByOwner } from '../../../api/games';
	import { getCookie } from '../../../utils/cookies';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let loading = true;
	let error: string | null = null;
		let games: Game[] = [];

	onMount(() => {
		(async () => {
			try {
						const token = getCookie('token');
						const ownerId = getCookie('user_id');
						if (!token || !ownerId) {
					await goto('/oauth');
					return;
				}
				games = await fetchGamesByOwner(ownerId, token);
			} catch (err) {
				const message = err instanceof Error ? err.message : String(err);
				error = message || 'Unable to load your games.';
			} finally {
				loading = false;
			}
		})();
	});
</script>

<section class="my-games-shell">
	<header class="my-games-header">
		<div>
			<h1>My games</h1>
			<p>Resume an existing story or launch a new quest with friends.</p>
		</div>
		<a class="create" href="/games/new">New game</a>
	</header>

	{#if loading}
		<div class="state">Fetching your library...</div>
	{:else if error}
		<div class="state error">{error}</div>
	{:else if games.length === 0}
		<div class="state">No games yet. Start your first adventure!</div>
	{:else}
		<div class="my-games-grid">
			{#each games as game (game.game_id)}
				<article class="game-item">
					<div class="item-head">
						<h2>{game.title}</h2>
						<span>{game.interactions.length} interactions</span>
					</div>
					<div class="item-actions">
						<a class="open" href={`/games/${game.game_id}`}>Open</a>
					</div>
				</article>
			{/each}
		</div>
	{/if}
</section>
