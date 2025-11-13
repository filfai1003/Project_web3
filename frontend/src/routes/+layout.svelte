<script lang="ts">
  import Header from '../components/header.svelte';
  import '../style/default.css';

  export let data: unknown;
  const initialAuth = (data as { initialAuth?: unknown })?.initialAuth ?? null;
</script>

<Header initialAuth={initialAuth} />

<main class="page-shell">
  <slot />
</main>
