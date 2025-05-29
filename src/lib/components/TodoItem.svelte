<script>
  import { createEventDispatcher } from 'svelte';
  import { scale, fly } from 'svelte/transition';
  
  export let todo;
  
  const dispatch = createEventDispatcher();
  
  let editing = false;
  let editText = todo.text;
  
  function startEdit() {
    editing = true;
    editText = todo.text;
  }
  
  function saveEdit() {
    if (editText.trim()) {
      dispatch('update', { ...todo, text: editText.trim() });
    }
    editing = false;
  }
  
  function cancelEdit() {
    editing = false;
    editText = todo.text;
  }
  
  function handleKeydown(event) {
    if (event.key === 'Enter') {
      saveEdit();
    } else if (event.key === 'Escape') {
      cancelEdit();
    }
  }
  
  function toggleComplete() {
    dispatch('update', { ...todo, completed: !todo.completed });
  }
  
  function deleteTodo() {
    dispatch('delete', todo.id);
  }

  function focusOnMount(node) {
    node.focus();
    return {};
  }
</script>

<div class="todo-item" class:completed={todo.completed} in:fly="{{ y: -20, duration: 300 }}" out:scale="{{ duration: 200 }}">
  <input 
    type="checkbox" 
    checked={todo.completed} 
    on:change={toggleComplete}
    class="checkbox"
  />
  
  {#if editing}
    <input 
      bind:value={editText}
      on:keydown={handleKeydown}
      on:blur={saveEdit}
      class="edit-input"
      use:focusOnMount
    />
  {:else}
    <span class="todo-text" on:dblclick={startEdit} role="button" tabindex="0">
      {todo.text}
    </span>
  {/if}
  
  <div class="todo-meta">
    <span class="priority priority-{todo.priority}">
      {todo.priority === 'high' ? '🔴' : todo.priority === 'medium' ? '🟡' : '🟢'}
    </span>
    <span class="category">{todo.category || '일반'}</span>
    <time class="created-at">
      {new Date(todo.createdAt).toLocaleDateString('ko-KR')}
    </time>
  </div>
  
  <div class="todo-actions">
    {#if !editing}
      <button class="action-btn edit-btn" on:click={startEdit}>✏️</button>
    {/if}
    <button class="action-btn delete-btn" on:click={deleteTodo}>🗑️</button>
  </div>
</div>

<style>
  .todo-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 0.5rem;
    margin-bottom: 0.5rem;
    transition: all 0.2s;
  }
  
  .todo-item:hover {
    border-color: var(--primary);
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
  }
  
  .todo-item.completed {
    opacity: 0.7;
  }
  
  .checkbox {
    width: 1.2rem;
    height: 1.2rem;
    accent-color: var(--primary);
  }
  
  .todo-text {
    flex: 1;
    cursor: pointer;
  }
  
  .completed .todo-text {
    text-decoration: line-through;
    color: var(--text-light);
  }
  
  .edit-input {
    flex: 1;
    padding: 0.5rem;
    border: 1px solid var(--primary);
    border-radius: 0.25rem;
    background: var(--bg);
    color: var(--text);
  }
  
  .todo-meta {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    font-size: 0.875rem;
    color: var(--text-light);
  }
  
  .category {
    background: var(--primary);
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
    font-size: 0.75rem;
  }
  
  .created-at {
    font-size: 0.75rem;
  }
  
  .todo-actions {
    display: flex;
    gap: 0.5rem;
  }
  
  .action-btn {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.25rem;
    border-radius: 0.25rem;
    transition: background-color 0.2s;
  }
  
  .action-btn:hover {
    background: var(--border);
  }
</style>