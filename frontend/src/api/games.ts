export type Interaction = {
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
