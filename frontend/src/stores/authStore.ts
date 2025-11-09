import { writable } from 'svelte/store';
import { getToken, setToken, clearToken } from '../utils/auth';

const initial = !!getToken();
export const loggedIn = writable<boolean>(initial);

export function loginWithToken(token: string) {
  setToken(token);
  loggedIn.set(true);
}

export function logout() {
  clearToken();
  loggedIn.set(false);
  try { window.location.href = '/'; } catch (e) {}
}

export function initAuth() {
  loggedIn.set(!!getToken());
}
