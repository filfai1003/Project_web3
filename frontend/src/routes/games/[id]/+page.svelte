<script lang="ts">
	import { onMount, tick } from 'svelte';
	import { get } from 'svelte/store';
	import { page } from '$app/stores';
	import '../../../style/game.css';
	import type { Interaction } from '../../../api/games';
	import { fetchGameById } from '../../../api/games';
	import { narratorPlayStream, playerPlay } from '../../../api/play';
	import { getCookie } from '../../../utils/cookies';

	let gameId = '';
	let title = '';
	let interactions: Interaction[] = [];

	let loadingGame = true;
	let processing = false;
	let streaming = false;
	let pageError: string | null = null;
	let composerError: string | null = null;

	let inputValue = '';
	let hasAuth = false;

	let feedEl: HTMLDivElement | null = null;
	let inputEl: HTMLTextAreaElement | null = null;

		let accessToken: string | undefined;
		let autoScroll = true;
		let cleanupFeedHandlers: (() => void) | null = null;
		let scrollAnchor: HTMLDivElement | null = null;

	onMount(() => {
		const { params } = get(page);
		gameId = params.id ?? '';
		refreshAuth();
		void hydrate('auto');

		const unsubscribe = page.subscribe((value) => {
			const nextId = value.params?.id ?? '';
			if (!nextId || nextId === gameId) return;
			gameId = nextId;
			refreshAuth();
			void hydrate('auto');
		});

		return () => {
					unsubscribe();
					if (cleanupFeedHandlers) {
						cleanupFeedHandlers();
						cleanupFeedHandlers = null;
					}
		};
	});

	async function hydrate(scrollBehavior: ScrollBehavior) {
		await loadGame(scrollBehavior);
		await tick();
		focusInput();
	}

	function refreshAuth() {
		try {
			accessToken = getCookie('token') ?? undefined;
			hasAuth = Boolean(accessToken);
		} catch (e) {
			accessToken = undefined;
			hasAuth = false;
		}
	}

	async function loadGame(scrollBehavior: ScrollBehavior = 'smooth') {
		if (!gameId) return;
		loadingGame = true;
		pageError = null;
		try {
			const game = await fetchGameById(gameId, accessToken);
			title = game.title;
			updateDocumentTitle(title);
			interactions = game.interactions ?? [];
			autoScroll = true;
		} catch (err) {
			const message = err instanceof Error ? err.message : String(err);
			pageError = message || 'Impossibile caricare la partita.';
		} finally {
			loadingGame = false;
		}

		if (!pageError) {
			await maybeAutoScroll(scrollBehavior);
		}
	}

	const hasInput = () => inputValue.trim().length > 0;

	async function submit() {
		if (processing) return;
		refreshAuth();
		composerError = null;

		const trimmed = inputValue.trim();
		if (!trimmed) {
			await callNarrator();
		} else {
			await sendInteraction(trimmed);
		}
	}

	async function sendInteraction(message: string) {
		if (!accessToken) {
			composerError = "Effettua il login per inviare un'interazione.";
			focusInput();
			return;
		}

		processing = true;
		const previous = [...interactions];
		const optimistic: Interaction = {
			sender: 'player',
			content: message,
			created_at: new Date().toISOString(),
		};
		interactions = [...previous, optimistic];
		inputValue = '';
		await tick();
		focusInput();
		await maybeAutoScroll('smooth');

		try {
			const response = await playerPlay(gameId, message, accessToken);
			const confirmed: Interaction = {
				sender: response.sender,
				content: response.content,
				created_at: response.created_at,
			};
			const insertIndex = previous.length;
			interactions = interactions.map((entry, index) => (index === insertIndex ? confirmed : entry));
		} catch (err) {
			const messageErr = err instanceof Error ? err.message : String(err);
			composerError = messageErr || 'Invio non riuscito.';
			interactions = previous;
			inputValue = message;
		} finally {
			processing = false;
			focusInput();
			await maybeAutoScroll('smooth');
		}
	}

	async function callNarrator() {
		if (streaming) return;
		processing = true;
		streaming = true;

		const narratorMessage: Interaction = {
			sender: 'narrator',
			content: '',
			created_at: new Date().toISOString(),
		};

		const base = [...interactions, narratorMessage];
		interactions = base;
		const messageIndex = base.length - 1;
		let aggregated = '';
		let rawBuffer = '';
		let serializedInteraction = '';
		let markerDetected = false;

		await tick();
		focusInput();
		await maybeAutoScroll('smooth');

		const markerToken = '\n__INTERACTION_JSON__\n';

		try {
			await narratorPlayStream(
				gameId,
				(chunk: string) => {
					rawBuffer += chunk;
					const markerIndex = rawBuffer.indexOf(markerToken);
					if (markerIndex !== -1) {
						markerDetected = true;
						aggregated = rawBuffer.slice(0, markerIndex);
						serializedInteraction = rawBuffer.slice(markerIndex + markerToken.length);
					} else {
						aggregated = rawBuffer;
					}
					narratorMessage.content = aggregated;
					interactions = interactions.map((entry, index) =>
						index === messageIndex ? { ...narratorMessage } : entry,
					);
					focusInput();
					if (autoScroll) {
						void scrollToBottom('smooth');
					}
				},
				accessToken,
			);
			if (markerDetected) {
				const payload = serializedInteraction.trim();
				if (payload) {
					try {
						const parsed = JSON.parse(payload) as Partial<Interaction>;
						if (parsed.content) narratorMessage.content = parsed.content;
						if (parsed.created_at) narratorMessage.created_at = parsed.created_at;
						if (parsed.sender) narratorMessage.sender = parsed.sender;
						if (parsed.interaction_id) narratorMessage.interaction_id = parsed.interaction_id;
					} catch (jsonError) {
						// ignore malformed payload, keep accumulated content
					}
				}
			}
			narratorMessage.content = narratorMessage.content.trim();
			interactions = interactions.map((entry, index) =>
				index === messageIndex ? { ...narratorMessage } : entry,
			);
		} catch (err) {
			const messageErr = err instanceof Error ? err.message : String(err);
			composerError = messageErr || 'Narratore non disponibile.';
			if (!aggregated) {
				interactions = interactions.slice(0, -1);
			}
		} finally {
			streaming = false;
			processing = false;
			focusInput();
			await maybeAutoScroll('smooth');
		}
	}

	function formatSender(sender: string) {
		if (sender.toLowerCase() === 'player') return 'Giocatore';
		if (sender.toLowerCase() === 'narrator') return 'Narratore';
		return sender;
	}

	function formatTimestamp(value: string | undefined) {
		if (!value) return '';
		const date = new Date(value);
		if (Number.isNaN(date.getTime())) return '';
		return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
	}

	function focusInput() {
		if (!inputEl) return;
		if (document.activeElement !== inputEl) {
			inputEl.focus();
		}
	}

		async function scrollToBottom(behavior: ScrollBehavior = 'smooth') {
			await tick();
			if (scrollAnchor) {
				scrollAnchor.scrollIntoView({ behavior, block: 'end' });
				return;
			}
			if (feedEl) {
				feedEl.scrollTo({ top: feedEl.scrollHeight, behavior });
			}
	}

	function handleKeyDown(event: KeyboardEvent) {
		if (event.key === 'Enter' && !event.ctrlKey) {
			event.preventDefault();
			void submit();
		}
	}

	function updateDocumentTitle(value: string) {
		try {
			document.title = value ? `${value} | Project Web3` : 'Project Web3';
		} catch (e) {
			// ignore document access issues (SSR)
		}
	}

	function maybeAutoScroll(behavior: ScrollBehavior = 'smooth') {
		if (!autoScroll) return Promise.resolve();
		return scrollToBottom(behavior);
	}

		function refreshFeedHandlers() {
			if (cleanupFeedHandlers) {
				cleanupFeedHandlers();
				cleanupFeedHandlers = null;
			}
			if (!feedEl) return;

			const node = feedEl;
			const onScroll = () => {
				autoScroll = isNearBottom(node);
			};
			node.addEventListener('scroll', onScroll, { passive: true });

			let observer: IntersectionObserver | null = null;
			if (scrollAnchor) {
				observer = new IntersectionObserver(
					(entries) => {
						autoScroll = entries.some((entry) => entry.isIntersecting);
					},
					{ root: node, threshold: 0.8 },
				);
				observer.observe(scrollAnchor);
			}

			autoScroll = isNearBottom(node);

			cleanupFeedHandlers = () => {
				node.removeEventListener('scroll', onScroll);
				if (observer) observer.disconnect();
			};
		}

		function isNearBottom(node: HTMLElement) {
			const threshold = 120;
			return node.scrollHeight - node.scrollTop - node.clientHeight <= threshold;
		}

		$: if (feedEl) {
			refreshFeedHandlers();
		}

		$: if (feedEl && scrollAnchor) {
			refreshFeedHandlers();
		}
</script>

<div class="game-shell">
	{#if loadingGame}
		<div class="state">Caricamento della partita...</div>
	{:else if pageError}
		<div class="state error">{pageError}</div>
	{:else}
			<div class="game-feed" bind:this={feedEl}>
			{#if interactions.length === 0}
				<div class="empty-state">Nessuna interazione ancora. Inizia tu oppure avvia il narratore.</div>
			{:else}
				{#each interactions as interaction, index (index)}
					<article class="message" class:player={interaction.sender.toLowerCase() === 'player'} class:narrator={interaction.sender.toLowerCase() !== 'player'}>
						<header class="message-meta">
							<span>{formatSender(interaction.sender)}</span>
							{#if formatTimestamp(interaction.created_at)}
								<time datetime={interaction.created_at}>{formatTimestamp(interaction.created_at)}</time>
							{/if}
						</header>
						<p class="message-content">{interaction.content}</p>
					</article>
				{/each}
			{/if}
				<div class="scroll-anchor" aria-hidden="true" bind:this={scrollAnchor}></div>
		</div>

		<form class="composer" on:submit|preventDefault={submit}>
			<label class="sr-only" for="interaction-input">Nuova interazione</label>
			<textarea
				id="interaction-input"
				bind:this={inputEl}
				bind:value={inputValue}
				rows="1"
				placeholder="Scrivi la prossima mossa oppure lascia parlare il narratore..."
				on:keydown={handleKeyDown}
				autocomplete="off"
			></textarea>
			<button
				type="submit"
				class="composer-action"
				data-mode={hasInput() ? 'send' : 'narrate'}
				disabled={processing}
			>
				<span class="action-label action-send">Invia interazione</span>
				<span class="action-label action-narrate">Avvia narratore</span>
			</button>
		</form>

		{#if !hasAuth}
			<p class="composer-hint">Accedi per registrare le tue mosse e mantenerle salvate.</p>
		{/if}

		{#if composerError}
			<p class="composer-error">{composerError}</p>
		{/if}
	{/if}
</div>
