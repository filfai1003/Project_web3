<script lang="ts">
  import '../style/default.css';
  import Header from '../components/header.svelte';

  export let data: any;
</script>

<Header initialAuth={data?.initialAuth} />

<main>
  <slot />
</main>
