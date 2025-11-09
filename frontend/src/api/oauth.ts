export type SignUpPayload = {
  username: string;
  email: string;
  password: string;
};

export type LoginPayload = {
  username?: string;
  email?: string;
  password: string;
};

export type Token = {
  access_token: string;
};

const BASE = 'http://127.0.0.1:8000';

async function handleResponse(res: Response) {
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`Request failed: ${res.status} ${res.statusText} ${text}`);
  }
  const data = await res.json().catch(() => ({}));
  return data;
}

export async function signup(payload: SignUpPayload): Promise<Token> {
  const res = await fetch(`${BASE}/auth/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return (await handleResponse(res)) as Token;
}

export async function login(payload: LoginPayload): Promise<Token> {
  const res = await fetch(`${BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return (await handleResponse(res)) as Token;
}

export async function authenticate(accessToken: string): Promise<Token> {
  const res = await fetch(`${BASE}/auth/authenticate`, {
    method: 'GET',
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  return (await handleResponse(res)) as Token;
}