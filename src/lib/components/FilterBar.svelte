<script>
  import { filter, stats } from '$lib/stores.js';
  
  const filters = [
    { value: 'all', label: '전체', icon: '📋' },
    { value: 'pending', label: '진행중', icon: '⏳' },
    { value: 'completed', label: '완료', icon: '✅' }
  ];
</script>

<div class="filter-bar">
  <div class="filter-buttons">
    {#each filters as filterOption}
      <button
        class="filter-btn"
        class:active={$filter === filterOption.value}
        on:click={() => filter.set(filterOption.value)}
      >
        <span class="filter-icon">{filterOption.icon}</span>
        <span class="filter-label">{filterOption.label}</span>
        <span class="filter-count">
          {filterOption.value === 'all' ? $stats.total : 
           filterOption.value === 'pending' ? $stats.pending : $stats.completed}
        </span>
      </button>
    {/each}
  </div>
  
  <div class="stats-summary">
    <span class="stat-item">
      총 {$stats.total}개 중 {$stats.completed}개 완료
    </span>
  </div>
</div>

<style>
  .filter-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding: 1rem;
    background: var(--surface);
    border-radius: 0.5rem;
    border: 1px solid var(--border);
  }
  
  .filter-buttons {
    display: flex;
    gap: 0.5rem;
  }
  
  .filter-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: none;
    border: 1px solid var(--border);
    border-radius: 0.5rem;
    cursor: pointer;
    color: var(--text);
    transition: all 0.2s;
  }
  
  .filter-btn:hover {
    background: var(--border);
  }
  
  .filter-btn.active {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
  }
  
  .filter-count {
    background: rgba(255, 255, 255, 0.2);
    padding: 0.25rem 0.5rem;
    border-radius: 1rem;
    font-size: 0.75rem;
    font-weight: 500;
  }
  
  .filter-btn.active .filter-count {
    background: rgba(255, 255, 255, 0.3);
  }
  
  .filter-btn:not(.active) .filter-count {
    background: var(--border);
    color: var(--text-light);
  }
  
  .stats-summary {
    color: var(--text-light);
    font-size: 0.875rem;
  }
</style>