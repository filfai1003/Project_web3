const BASE = 'http://127.0.0.1:8000';

export type PlayMessageOut = {
  interaction_id: string;
  sender: string;
  content: string;
  created_at: string;
};

export async function playerPlay(gameId: string, message: string): Promise<PlayMessageOut> {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };

  const body = { game_id: gameId, message };
  const res = await fetch(`${BASE}/play/player`, { method: 'POST', headers, body: JSON.stringify(body), credentials: 'include' });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`Failed to send player message: ${res.status} ${res.statusText} ${text}`);
  }
  const data = await res.json();
  return data as PlayMessageOut;
}

export async function narratorPlay(gameId: string): Promise<string> {
  const res = await fetch(`${BASE}/play/narrator/${encodeURIComponent(gameId)}`, { method: 'GET', credentials: 'include' });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`Failed to request narrator: ${res.status} ${res.statusText} ${text}`);
  }
  const data = await res.text();
  return data;
}

export async function narratorPlayStream(gameId: string, onMessage: (message: string) => void): Promise<void> {
  const res = await fetch(`${BASE}/play/narrator/${encodeURIComponent(gameId)}`, { method: 'GET', credentials: 'include' });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`Failed to request narrator: ${res.status} ${res.statusText} ${text}`);
  }

  const reader = res.body?.getReader();
  if (!reader) {
    throw new Error('Failed to get reader from response body');
  }

  const decoder = new TextDecoder('utf-8');
  let done = false;

  while (!done) {
    const { value, done: readerDone } = await reader.read();
    done = readerDone;
    if (value) {
      const chunk = decoder.decode(value, { stream: true });
      onMessage(chunk);
    }
  }
}
