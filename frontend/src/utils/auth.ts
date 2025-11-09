export const TOKEN_KEY = 'access_token';

export function setToken(token: string) {
  try {
    localStorage.setItem(TOKEN_KEY, token);
  } catch (e) {}
}

export function getToken(): string | null {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch (e) { return null; }
}

export function clearToken() {
  try { localStorage.removeItem(TOKEN_KEY); } catch (e) {}
}

export function isAuthenticated(): boolean {
  return !!getToken();
}
