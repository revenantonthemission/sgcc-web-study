<script>
  import { createEventDispatcher } from 'svelte';
  import { slide } from 'svelte/transition';
  
  const dispatch = createEventDispatcher();
  
  let text = '';
  let priority = 'medium';
  let category = '';
  let showAdvanced = false;
  
  const categories = ['업무', '개인', '쇼핑', '건강', '학습'];
  
  function handleSubmit() {
    if (text.trim()) {
      dispatch('submit', {
        text: text.trim(),
        priority,
        category: category || '일반',
        completed: false,
        createdAt: new Date().toISOString()
      });
      
      text = '';
      priority = 'medium';
      category = '';
      showAdvanced = false;
    }
  }
  
  function handleKeydown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSubmit();
    }
  }
</script>

<form class="todo-form" on:submit|preventDefault={handleSubmit}>
  <div class="main-input">
    <input
      bind:value={text}
      on:keydown={handleKeydown}
      placeholder="새로운 할 일을 입력하세요..."
      class="text-input"
      required
    />
    <button type="button" class="advanced-toggle" on:click={() => showAdvanced = !showAdvanced}>
      ⚙️
    </button>
    <button type="submit" class="submit-btn" disabled={!text.trim()}>
      추가
    </button>
  </div>
  
  {#if showAdvanced}
    <div class="advanced-options" transition:slide="{{ duration: 200 }}">
      <div class="option-group">
        <label for="priority">우선순위:</label>
        <select bind:value={priority} id="priority" class="select-input">
          <option value="low">낮음</option>
          <option value="medium">보통</option>
          <option value="high">높음</option>
        </select>
      </div>
      
      <div class="option-group">
        <label for="category">카테고리:</label>
        <select bind:value={category} id="category" class="select-input">
          <option value="">일반</option>
          {#each categories as cat}
            <option value={cat}>{cat}</option>
          {/each}
        </select>
      </div>
    </div>
  {/if}
</form>

<style>
  .todo-form {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 0.5rem;
    padding: 1rem;
    margin-bottom: 2rem;
  }
  
  .main-input {
    display: flex;
    gap: 0.5rem;
    align-items: center;
  }
  
  .text-input {
    flex: 1;
    padding: 0.75rem;
    border: 1px solid var(--border);
    border-radius: 0.5rem;
    background: var(--bg);
    color: var(--text);
    font-size: 1rem;
  }
  
  .text-input:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
  }
  
  .advanced-toggle {
    background: none;
    border: 1px solid var(--border);
    padding: 0.75rem;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .advanced-toggle:hover {
    background: var(--border);
  }
  
  .submit-btn {
    background: var(--primary);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    cursor: pointer;
    font-weight: 500;
    transition: background-color 0.2s;
  }
  
  .submit-btn:hover:not(:disabled) {
    background: var(--primary-dark);
  }
  
  .submit-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .advanced-options {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
  }
  
  .option-group {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .option-group label {
    font-size: 0.875rem;
    color: var(--text-light);
  }
  
  .select-input {
    padding: 0.5rem;
    border: 1px solid var(--border);
    border-radius: 0.25rem;
    background: var(--bg);
    color: var(--text);
  }
</style>