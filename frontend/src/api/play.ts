const BASE = 'http://127.0.0.1:8000';

export type PlayMessageOut = {
  interaction_id: string;
  sender: string;
  content: string;
  created_at: string;
};

export async function playerPlay(gameId: string, message: string, accessToken?: string): Promise<PlayMessageOut> {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (accessToken) headers['Authorization'] = `Bearer ${accessToken}`;

  const body = { game_id: gameId, message };
  const res = await fetch(`${BASE}/play/player`, { method: 'POST', headers, body: JSON.stringify(body) });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`Failed to send player message: ${res.status} ${res.statusText} ${text}`);
  }
  const data = await res.json();
  return data as PlayMessageOut;
}

export async function narratorPlay(gameId: string, accessToken?: string): Promise<string> {
  const headers: Record<string, string> = {};
  if (accessToken) headers['Authorization'] = `Bearer ${accessToken}`;

  const res = await fetch(`${BASE}/play/narrator/${encodeURIComponent(gameId)}`, { method: 'GET', headers });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`Failed to request narrator: ${res.status} ${res.statusText} ${text}`);
  }
  const data = await res.text();
  return data;
}
