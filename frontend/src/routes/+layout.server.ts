import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ cookies }) => {
  try {
    const token = cookies.get('token');
    const username = cookies.get('username');
    const email = cookies.get('email');
    const user_id = cookies.get('user_id');

    const profile = username || email || user_id ? {
      username: username ?? undefined,
      email: email ?? undefined,
      user_id: user_id ?? undefined
    } : null;

    return {
      initialAuth: {
        loggedIn: !!token,
        profile
      }
    };
  } catch (e) {
    return { initialAuth: { loggedIn: false, profile: null } };
  }
};
