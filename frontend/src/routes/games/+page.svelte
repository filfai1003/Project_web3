<script lang="ts">
	import { onMount } from 'svelte';
	import '../../style/games.css';
	import GameCard from '../../components/game_card.svelte';
	import type { Game } from '../../api/games';
	import { fetchGames } from '../../api/games';

	let games: Game[] = [];
	let loading = true;
	let error: string | null = null;

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

