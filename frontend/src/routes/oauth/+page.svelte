<script lang="ts">
	import '../../style/oauth.css';
	import type { LoginPayload, SignUpPayload, Token } from '../../api/oauth';
	import { login, signup } from '../../api/oauth';
	import { setUserProfile } from '../../stores/authStore';
	import { getCookie } from '../../utils/cookies';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	type Mode = 'login' | 'signup';

	let mode: Mode = 'login';
	let loading = false;
	let error: string | null = null;

	let loginForm = {
		identifier: '',
		password: ''
	};

	let signupForm: SignUpPayload = {
		username: '',
		email: '',
		password: ''
	};

	onMount(() => {
		try {
					// if profile cookies exist, redirect to user's games
					if (getCookie('username') || getCookie('user_id')) {
							void goto('/games?view=mine');
					}
		} catch (e) {}
	});

	function switchMode(next: Mode) {
		if (mode === next) return;
		mode = next;
		error = null;
	}

	async function submit() {
		if (loading) return;
		error = null;
		loading = true;

		try {
			let token: Token;

			if (mode === 'login') {
				const identifier = loginForm.identifier.trim();
				if (!identifier) throw new Error('Enter your username or email.');
				const payload: LoginPayload = { password: loginForm.password };
				if (identifier.includes('@')) payload.email = identifier;
				else payload.username = identifier;
				token = await login(payload);
			} else {
				const payload: SignUpPayload = {
					username: signupForm.username.trim(),
					email: signupForm.email.trim(),
					password: signupForm.password
				};
				if (!payload.username || !payload.email) {
					throw new Error('Fill in all the fields to create an account.');
				}
				token = await signup(payload);
			}

			// server sets HttpOnly access token cookie; frontend receives profile in response
			setUserProfile({ user_id: token.user_id, username: token.username, email: token.email });
			await goto('/games?view=mine');
		} catch (err) {
			const message = err instanceof Error ? err.message : String(err);
			error = message || 'Unable to authenticate. Please try again.';
		} finally {
			loading = false;
		}
	}
</script>

<section class="auth-shell">
	<div class="auth-card">
		<header class="auth-header">
			<h1>Welcome back</h1>
			<p>Access collaborative adventures or create a new account in minutes.</p>
		</header>

		<div class="auth-tabs" role="tablist">
			<button type="button" class:active={mode === 'login'} on:click={() => switchMode('login')}>
				Login
			</button>
			<button type="button" class:active={mode === 'signup'} on:click={() => switchMode('signup')}>
				Sign up
			</button>
		</div>

		<form class="auth-form" on:submit|preventDefault={submit}>
			{#if mode === 'login'}
				<label>
					<span>Username or email</span>
					<input
						type="text"
						autocomplete="username"
						placeholder="player or player@email.com"
						bind:value={loginForm.identifier}
						required
					/>
				</label>
				<label>
					<span>Password</span>
					<input
						type="password"
						autocomplete="current-password"
						placeholder="••••••••"
						bind:value={loginForm.password}
						required
					/>
				</label>
			{:else}
				<label>
					<span>Username</span>
					<input
						type="text"
						autocomplete="username"
						placeholder="Choose a handle"
						bind:value={signupForm.username}
						required
					/>
				</label>
				<label>
					<span>Email</span>
					<input
						type="email"
						autocomplete="email"
						placeholder="name@email.com"
						bind:value={signupForm.email}
						required
					/>
				</label>
				<label>
					<span>Password</span>
					<input
						type="password"
						autocomplete="new-password"
						placeholder="Create a secure password"
						bind:value={signupForm.password}
						minlength="8"
						required
					/>
				</label>
			{/if}

			{#if error}
				<p class="auth-error">{error}</p>
			{/if}

			<button type="submit" class="auth-submit" disabled={loading}>
				{#if loading}
					Processing...
				{:else if mode === 'login'}
					Log in
				{:else}
					Create account
				{/if}
			</button>
		</form>
	</div>
</section>
