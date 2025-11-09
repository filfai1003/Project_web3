<script lang="ts">
  import '../../style/oauth.css';
  import type { LoginPayload, SignUpPayload } from '../../api/oauth';
  import { login, signup } from '../../api/oauth';
  import { loginWithToken } from '../../stores/authStore';

  let username = '';
  let email = '';
  let identifier = '';
  let password = '';
  let error: string | null = null;
  let loading = false;
  let isSignup = false;

  async function submit() {
    error = null;
    loading = true;
    try {
      if (isSignup) {
          if (username.includes('@')) {
            throw new Error("Username must not contain '@'");
          }
          const payload: SignUpPayload = { username, email, password };
            const t = await signup(payload);
          loginWithToken(t.access_token);
      } else {
          const id = identifier.trim();
          const payload: LoginPayload = id.includes('@') ? { email: id, password } : { username: id, password };
          const t = await login(payload);
        loginWithToken(t.access_token);
      }
      window.location.href = '/';
    } catch (e) {
      error = (e as Error)?.message ?? String(e);
    } finally { loading = false; }
  }

  function toggleMode() {
    isSignup = !isSignup;
    error = null;
    password = '';
    identifier = '';
    username = '';
    email = '';
  }
</script>

<div class="oauth-container">
  <div class="oauth-card">
    <h1>{isSignup ? 'Create an account' : 'Welcome back'}</h1>
    <p class="muted">{isSignup ? 'Sign up to start a new adventure.' : 'Sign in to continue.'}</p>

    <form class="oauth-form" on:submit|preventDefault={submit}>
      {#if isSignup}
        <div class="field">
          <label>Username
            <input type="text" bind:value={username} placeholder="choose a username" required pattern="^[^@]+$" title="Username must not contain '@'" />
          </label>
        </div>
        <div class="field">
          <label>Email
            <input type="email" bind:value={email} placeholder="you@example.com" required />
          </label>
        </div>
      {:else}
        <div class="field">
          <label>Username or email
            <input type="text" bind:value={identifier} placeholder="username or email" required />
          </label>
        </div>
      {/if}

      <div class="field">
        <label>Password
          <input type="password" bind:value={password} placeholder="password" required />
        </label>
      </div>

      <div class="actions">
        <button class="btn primary" disabled={loading}>
          {#if loading}{isSignup ? 'Creating...' : 'Signing in...'}{:else}{isSignup ? 'Sign up' : 'Login'}{/if}
        </button>
        <button type="button" class="btn ghost" on:click={toggleMode} disabled={loading}>
          {isSignup ? 'Back to login' : 'Create account'}
        </button>
      </div>

      {#if error}
        <p class="error">{error}</p>
      {/if}
    </form>
  </div>
</div>
