<script>
  import { onMount } from 'svelte';
  import { theme } from '$lib/stores.js';
  import Header from '$lib/components/Header.svelte';
  import '../app.css';
  
  onMount(() => {
    // 테마 적용
    const unsubscribe = theme.subscribe(value => {
      if (typeof document !== 'undefined') {
        document.documentElement.setAttribute('data-theme', value);
      }
    });
    
    return unsubscribe;
  });
</script>

<div class="app">
  <Header />
  <main class="main">
    <slot />
  </main>
</div>

<style>
  .app {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }
  
  .main {
    flex: 1;
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
    width: 100%;
  }
</style>
