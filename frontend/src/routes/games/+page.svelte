<script lang="ts">
	import { onMount } from 'svelte';
	import '../../style/games.css';
	import GameCard from '../../components/game_card.svelte';
	import type { Game } from '../../api/games';
	import { fetchGames } from '../../api/games';
	import { getCookie } from '../../utils/cookies';

	let games: Game[] = [];
	let loading = true;
	let error: string | null = null;

	function createNew() {
		const token = getCookie('token');
		if (!token) {
			window.location.href = '/oauth';
			return;
		}
		window.location.href = '/games/new';
	}

	onMount(async () => {
		try {
			games = await fetchGames();
		} catch (e) {
			error = (e as Error)?.message ?? String(e);
		} finally {
			loading = false;
		}
	});
</script>

<div class="games-container">
	<div class="grid-header">
		<h1>Games</h1>
		<div class="muted">{games.length} games</div>
		<button class="create-btn" on:click={createNew}>Create new</button>
	</div>

	{#if loading}
		<p class="loader">Loading games...</p>
	{:else if error}
		<p class="muted">Error: {error}</p>
	{:else if games.length === 0}
		<p class="muted">No games found.</p>
	{:else}
			<div class="game-list">
				{#each games as g}
					<GameCard game={g} />
				{/each}
			</div>
	{/if}
</div>

