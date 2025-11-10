<script lang="ts">
	import '../../../style/game.css';
	import type { Game, Interaction } from '../../../api/games';
	import { fetchGameById } from '../../../api/games';
	import { narratorPlayStream, playerPlay } from '../../../api/play';
	import { getCookie } from '../../../utils/cookies';
	import { goto } from '$app/navigation';
	import { afterUpdate, onMount } from 'svelte';

	export let params: { id: string };

	let game: Game | null = null;
	let conversation: Interaction[] = [];
	let loading = true;
	let error: string | null = null;
	let actionError: string | null = null;
	let message = '';
	let sending = false;
	let streaming = false;
	let messagesEl: HTMLDivElement | null = null;

	afterUpdate(() => {
		if (messagesEl) {
			messagesEl.scrollTo({ top: messagesEl.scrollHeight, behavior: 'smooth' });
		}
	});

	onMount(() => {
		void loadGame();
	});

	async function loadGame() {
		try {
			loading = true;
			error = null;
			const token = getCookie('token');
			if (!token) {
				await goto('/oauth');
				return;
			}
			await refreshConversation(token, true);
		} catch (err) {
			const messageText = err instanceof Error ? err.message : String(err);
			error = messageText || 'Unable to open this game.';
		} finally {
			loading = false;
		}
	}

	async function refreshConversation(token: string, replaceGame = false) {
		const latest = await fetchGameById(params.id, token);
		if (replaceGame || !game) {
			game = latest;
		} else {
			game = { ...game, ...latest };
		}
		conversation = latest.interactions ?? [];
	}

	function senderLabel(sender: string) {
		if (!sender) return 'Narrator';
		const lower = sender.toLowerCase();
		if (lower.includes('player')) return 'You';
		if (lower.includes('narrator')) return 'Narrator';
		return sender;
	}

	function senderClass(sender: string) {
		return sender && sender.toLowerCase().includes('player') ? 'player' : 'narrator';
	}

	function formatTime(value: string) {
		try {
			const date = new Date(value);
			return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
		} catch (e) {
			return '';
		}
	}

	async function sendMessage() {
		if (!game || sending) return;
		const trimmed = message.trim();
		if (!trimmed) return;
		actionError = null;
		const token = getCookie('token');
		if (!token) {
			await goto('/oauth');
			return;
		}
		sending = true;
		try {
			const reply = await playerPlay(game.game_id, trimmed, token);
			conversation = [...conversation, { sender: reply.sender, content: reply.content, created_at: reply.created_at }];
			message = '';
			await refreshConversation(token);
		} catch (err) {
			const messageText = err instanceof Error ? err.message : String(err);
			actionError = messageText || 'Unable to send your message.';
		} finally {
			sending = false;
		}
	}

	async function startNarrator() {
		if (!game || streaming) return;
		actionError = null;
		const token = getCookie('token');
		if (!token) {
			await goto('/oauth');
			return;
		}
		streaming = true;
		const streamIndex = conversation.length;
		const startEntry: Interaction = {
			sender: 'Narrator',
			content: '',
			created_at: new Date().toISOString()
		};
		conversation = [...conversation, startEntry];
		try {
			await narratorPlayStream(game.game_id, (chunk) => {
				conversation = conversation.map((entry, index) =>
					index === streamIndex ? { ...entry, content: entry.content + chunk } : entry
				);
			}, token);
			await refreshConversation(token);
		} catch (err) {
			const messageText = err instanceof Error ? err.message : String(err);
			actionError = messageText || 'Narrator could not complete the response.';
		} finally {
			streaming = false;
		}
	}
</script>

{#if loading}
	<div class="game-state">Loading game...</div>
{:else if error}
	<div class="game-state error">{error}</div>
{:else if !game}
	<div class="game-state error">Game not found.</div>
{:else}
	<section class="game-shell">
		<header class="game-header">
			<div>
				<h1>{game.title}</h1>
				<p>Interact with the narrator to keep the story alive.</p>
			</div>
			<div class="game-actions">
				<button type="button" class="narrator" on:click={startNarrator} disabled={streaming}>
					{#if streaming}
						Narrator streaming...
					{:else}
						Ask narrator
					{/if}
				</button>
			</div>
		</header>

		{#if actionError}
			<p class="game-alert">{actionError}</p>
		{/if}

		<div class="game-grid">
					<div class="conversation" bind:this={messagesEl}>
						{#each conversation as entry, index (index)}
					<div class={`bubble ${senderClass(entry.sender)}`}>
						<div class="bubble-meta">
							<span>{senderLabel(entry.sender)}</span>
							{#if entry.created_at}
								<time>{formatTime(entry.created_at)}</time>
							{/if}
						</div>
						<p>{entry.content}</p>
					</div>
				{/each}
				{#if conversation.length === 0}
					<div class="conversation-empty">No messages yet. Say hi to begin the story.</div>
				{/if}
			</div>

			<form class="composer" on:submit|preventDefault={sendMessage}>
				<label>
					<span>Your move</span>
					<textarea
						rows="4"
						placeholder="Describe your next action..."
						bind:value={message}
						required
					></textarea>
				</label>
				<div class="composer-actions">
					<button type="submit" class="send" disabled={sending}>
						{#if sending}
							Sending...
						{:else}
							Send message
						{/if}
					</button>
					<button type="button" class="narrator" on:click={startNarrator} disabled={streaming}>
						{#if streaming}
							Narrator streaming...
						{:else}
							Ask narrator
						{/if}
					</button>
				</div>
			</form>
		</div>
	</section>
{/if}
