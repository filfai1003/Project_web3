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
	const res = await fetch(`${BASE}/game/`, { method: 'GET' });
	if (!res.ok) {
		const text = await res.text().catch(() => '');
		throw new Error(`Failed to fetch games: ${res.status} ${res.statusText} ${text}`);
	}
	const data = await res.json();
	return data as Game[];
}

export async function fetchGamesByOwner(ownerId: string, accessToken?: string): Promise<Game[]> {
	const headers: Record<string, string> = {};
	if (accessToken) headers['Authorization'] = `Bearer ${accessToken}`;

	const res = await fetch(`${BASE}/game/owner/${ownerId}`, { method: 'GET', headers });
	if (!res.ok) {
		const text = await res.text().catch(() => '');
		throw new Error(`Failed to fetch owner games: ${res.status} ${res.statusText} ${text}`);
	}
	const data = await res.json().catch(() => []);
	return data as Game[];
}

export async function createGame(title: string, accessToken?: string): Promise<Game> {
	const headers: Record<string, string> = { 'Content-Type': 'application/json' };
	if (accessToken) headers['Authorization'] = `Bearer ${accessToken}`;

	const url = `${BASE}/game/?title=${encodeURIComponent(title)}`;
	const res = await fetch(url, { method: 'POST', headers });
	if (!res.ok) {
		const text = await res.text().catch(() => '');
		throw new Error(`Failed to create game: ${res.status} ${res.statusText} ${text}`);
	}
	const data = await res.json();
	return data as Game;
}

export async function fetchGameById(gameId: string, accessToken?: string): Promise<Game> {
	const headers: Record<string, string> = {};
	if (accessToken) headers['Authorization'] = `Bearer ${accessToken}`;

	const res = await fetch(`${BASE}/game/${encodeURIComponent(gameId)}`, { method: 'GET', headers });
	if (!res.ok) {
		const text = await res.text().catch(() => '');
		throw new Error(`Failed to fetch game: ${res.status} ${res.statusText} ${text}`);
	}
	const data = await res.json();
	return data as Game;
}

export async function deleteGameById(gameId: string, accessToken?: string): Promise<void> {
	const headers: Record<string, string> = {};
	if (accessToken) headers['Authorization'] = `Bearer ${accessToken}`;

	const res = await fetch(`${BASE}/game/${encodeURIComponent(gameId)}`, { method: 'DELETE', headers });
	if (!res.ok) {
		const text = await res.text().catch(() => '');
		throw new Error(`Failed to delete game: ${res.status} ${res.statusText} ${text}`);
	}
}
