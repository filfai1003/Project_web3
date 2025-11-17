import { writable } from 'svelte/store';
import { setCookie, getCookie, deleteCookie } from '../utils/cookies';
import { logout as apiLogout } from '../api/oauth';

const initial = !!getCookie('username') || !!getCookie('user_id');
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
  // mark as logged in in client state
  loggedIn.set(true);
}

export function clearUserProfile() {
  profile.set(null);
  try {
    deleteCookie('username');
    deleteCookie('email');
    deleteCookie('user_id');
    // token is HttpOnly and cleared via server logout
  } catch (e) {}
  loggedIn.set(false);
}

export function restoreProfileFromCookie() {
  try {
    const username = getCookie('username');
    const email = getCookie('email');
    const user_id = getCookie('user_id');
    if (username || email || user_id) {
      loggedIn.set(true);
    }
    if (username || email || user_id) {
      profile.set({ username: username ?? undefined, email: email ?? undefined, user_id: user_id ?? undefined });
    }
  } catch (e) {
  }
}

export function logout() {
  // call server logout to clear HttpOnly cookie, then clear client state
  try {
    void apiLogout();
  } catch (e) {}
  clearUserProfile();
  loggedIn.set(false);
  try { window.location.href = '/'; } catch (e) {}
}

export function initAuth() {
  loggedIn.set(!!getCookie('username') || !!getCookie('user_id'));
}
