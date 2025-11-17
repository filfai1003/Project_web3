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
  user_id: string;
  username: string;
  email?: string;
};

const BASE = "http://127.0.0.1:8000";

async function handleResponse(res: Response) {
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    // Try to parse JSON error body, but be resilient to empty/non-JSON responses
    try {
      if (text) {
        const errorData = JSON.parse(text);
        const message = errorData?.detail ?? errorData?.message ?? JSON.stringify(errorData);
        throw new Error(message || res.statusText || `HTTP ${res.status}`);
      }
    } catch (err) {
      // fall through to throw a reasonable message below
    }
    // fallback to raw text or status text
    throw new Error(text || res.statusText || `HTTP ${res.status}`);
  }
  try {
    const data = await res.json();
    return data;
  } catch {
    return {};
  }
}

export async function signup(payload: SignUpPayload): Promise<Token> {
  const res = await fetch(`${BASE}/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: 'include',
    body: JSON.stringify(payload),
  });
  return (await handleResponse(res)) as Token;
}

export async function login(payload: LoginPayload): Promise<Token> {
  const res = await fetch(`${BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: 'include',
    body: JSON.stringify(payload),
  });
  return (await handleResponse(res)) as Token;
}

export async function authenticate(): Promise<Token> {
  const res = await fetch(`${BASE}/auth/authenticate`, {
    method: "GET",
    credentials: 'include',
  });
  return (await handleResponse(res)) as Token;
}

export async function logout(): Promise<void> {
  const res = await fetch(`${BASE}/auth/logout`, {
    method: 'POST',
    credentials: 'include',
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`Failed to logout: ${res.status} ${res.statusText} ${text}`);
  }
}
