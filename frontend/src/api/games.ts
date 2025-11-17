export type Interaction = {
	interaction_id?: string;
	sender: string;
	content: string;
	created_at: string;
};

export type Game = {
	game_id: string;
	owner_id: string;
	title: string;
	interactions: Interaction[];
};

const BASE = 'http://127.0.0.1:8000';

export async function fetchGames(): Promise<Game[]> {
	const res = await fetch(`${BASE}/game/`, { method: 'GET', credentials: 'include' });
	if (!res.ok) {
		const text = await res.text().catch(() => '');
		throw new Error(`Failed to fetch games: ${res.status} ${res.statusText} ${text}`);
	}
	const data = await res.json();
	return data as Game[];
}

export async function fetchGamesByOwner(ownerId: string): Promise<Game[]> {
	const res = await fetch(`${BASE}/game/owner/${ownerId}`, { method: 'GET', credentials: 'include' });
	if (!res.ok) {
		const text = await res.text().catch(() => '');
		throw new Error(`Failed to fetch owner games: ${res.status} ${res.statusText} ${text}`);
	}
	const data = await res.json().catch(() => []);
	return data as Game[];
}

export async function createGame(title: string): Promise<Game> {
	const headers: Record<string, string> = { 'Content-Type': 'application/json' };

	const url = `${BASE}/game/?title=${encodeURIComponent(title)}`;
	const res = await fetch(url, { method: 'POST', headers, credentials: 'include' });
	if (!res.ok) {
		const text = await res.text().catch(() => '');
		throw new Error(`Failed to create game: ${res.status} ${res.statusText} ${text}`);
	}
	const data = await res.json();
	return data as Game;
}

export async function fetchGameById(gameId: string): Promise<Game> {
	const res = await fetch(`${BASE}/game/${encodeURIComponent(gameId)}`, { method: 'GET', credentials: 'include' });
	if (!res.ok) {
		const text = await res.text().catch(() => '');
		throw new Error(`Failed to fetch game: ${res.status} ${res.statusText} ${text}`);
	}
	const data = await res.json();
	return data as Game;
}

export async function deleteGameById(gameId: string): Promise<void> {
	const res = await fetch(`${BASE}/game/${encodeURIComponent(gameId)}`, { method: 'DELETE', credentials: 'include' });
	if (!res.ok) {
		const text = await res.text().catch(() => '');
		throw new Error(`Failed to delete game: ${res.status} ${res.statusText} ${text}`);
	}
}
