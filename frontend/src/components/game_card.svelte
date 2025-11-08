<script lang="ts">
	import type { Game } from '../api/games';

	// backend GameOut shape: { game_id, owner_id, title, interactions }
	export let game: Game;
</script>

<article class="game-card">
		<h2>
			<a href={'/games/' + game.game_id}>{game.title}</a>
		</h2>
	<p class="muted">Owner: {game.owner_id} · Interactions: {game.interactions?.length ?? 0}</p>
</article>

<style>
	.game-card a { color: inherit; text-decoration: none; }
	.game-card a:hover { text-decoration: underline; }
</style>
