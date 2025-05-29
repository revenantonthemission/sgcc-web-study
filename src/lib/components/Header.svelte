<script>
  import { theme } from '$lib/stores.js';
  
  function toggleTheme() {
    theme.update(t => t === 'light' ? 'dark' : 'light');
  }
</script>

<header class="header">
  <div class="container">
    <h1>할 일 관리</h1>
    <nav>
      <a href="/" class="nav-link">홈</a>
      <a href="/stats" class="nav-link">통계</a>
      <a href="/about" class="nav-link">정보</a>
      <button class="theme-toggle" on:click={toggleTheme}>
        {$theme === 'light' ? '🌙' : '☀️'}
      </button>
    </nav>
  </div>
</header>

<style>
  .header {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 1rem 0;
  }
  
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  h1 {
    margin: 0;
    color: var(--primary);
  }
  
  nav {
    display: flex;
    gap: 1rem;
    align-items: center;
  }
  
  .nav-link {
    color: var(--text);
    text-decoration: none;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    transition: background-color 0.2s;
  }
  
  .nav-link:hover {
    background: var(--border);
  }
  
  .theme-toggle {
    background: none;
    border: 1px solid var(--border);
    padding: 0.5rem;
    border-radius: 0.5rem;
    cursor: pointer;
    font-size: 1.2rem;
  }
</style>