import { writable } from 'svelte/store';
import { setCookie, getCookie, deleteCookie } from '../utils/cookies';

const initial = !!getCookie('token');
export const loggedIn = writable<boolean>(initial);

export type UserProfile = { user_id?: string; username?: string; email?: string } | null;
export const profile = writable<UserProfile>(null);

export function setUserProfile(p: UserProfile) {
  profile.set(p);
  try {
    if (p?.username) setCookie('username', p.username, 30);
    if (p?.email) setCookie('email', p.email, 30);
    if (p?.user_id) setCookie('user_id', String(p.user_id), 30);
  } catch (e) {}
}

export function clearUserProfile() {
  profile.set(null);
  try {
    deleteCookie('username');
    deleteCookie('email');
    deleteCookie('user_id');
    deleteCookie('token');
  } catch (e) {}
}

export function restoreProfileFromCookie() {
  try {
    const token = getCookie('token');
    const username = getCookie('username');
    const email = getCookie('email');
    const user_id = getCookie('user_id');
    if (token) {
      loggedIn.set(true);
    }
    if (username || email || user_id) {
      profile.set({ username: username ?? undefined, email: email ?? undefined, user_id: user_id ?? undefined });
    }
  } catch (e) {
  }
}

export function loginWithToken(token: string) {
  try { setCookie('token', token, 30); } catch (e) {}
  loggedIn.set(true);
}

export function logout() {
  clearUserProfile();
  loggedIn.set(false);
  try { window.location.href = '/'; } catch (e) {}
}

export function initAuth() {
  loggedIn.set(!!getCookie('token'));
}
