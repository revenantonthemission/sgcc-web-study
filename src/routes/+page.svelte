<script>
  import { onMount } from 'svelte';
  import { todos, filteredTodos, loading, notifications } from '$lib/stores.js';
  import { fetchTodos, createTodo, updateTodo, deleteTodo } from '$lib/api.js';
  import TodoForm from '$lib/components/TodoForm.svelte';
  import TodoItem from '$lib/components/TodoItem.svelte';
  import FilterBar from '$lib/components/FilterBar.svelte';
  import { flip } from 'svelte/animate';
  import { fade } from 'svelte/transition';
  
  onMount(async () => {
    await loadTodos();
  });
  
  async function loadTodos() {
    loading.set(true);
    try {
      const data = await fetchTodos();
      todos.set(data);
    } catch (error) {
      addNotification('할 일 목록을 불러오는데 실패했습니다.', 'error');
    } finally {
      loading.set(false);
    }
  }
  
  async function handleCreateTodo(event) {
    try {
      const newTodo = await createTodo(event.detail);
      todos.update(list => [...list, newTodo]);
      addNotification('할 일이 추가되었습니다.', 'success');
    } catch (error) {
      addNotification('할 일 추가에 실패했습니다.', 'error');
    }
  }
  
  async function handleUpdateTodo(event) {
    const { id, ...updates } = event.detail;
    try {
      const updatedTodo = await updateTodo(id, updates);
      todos.update(list => list.map(todo => todo.id === id ? updatedTodo : todo));
      addNotification('할 일이 수정되었습니다.', 'success');
    } catch (error) {
      addNotification('할 일 수정에 실패했습니다.', 'error');
    }
  }
  
  async function handleDeleteTodo(event) {
    const id = event.detail;
    try {
      await deleteTodo(id);
      todos.update(list => list.filter(todo => todo.id !== id));
      addNotification('할 일이 삭제되었습니다.', 'success');
    } catch (error) {
      addNotification('할 일 삭제에 실패했습니다.', 'error');
    }
  }
  
  function addNotification(message, type = 'info') {
    const id = Date.now();
    notifications.update(list => [...list, { id, message, type }]);
    setTimeout(() => {
      notifications.update(list => list.filter(n => n.id !== id));
    }, 3000);
  }
</script>

<svelte:head>
  <title>할 일 관리 - 홈</title>
  <meta name="description" content="SvelteKit으로 만든 할 일 관리 애플리케이션" />
</svelte:head>

<div class="page">
  <h1>할 일 관리</h1>
  
  <TodoForm on:submit={handleCreateTodo} />
  
  <FilterBar />
  
  {#if $loading}
    <div class="loading" transition:fade>
      <div class="spinner"></div>
      <p>로딩 중...</p>
    </div>
  {:else if $filteredTodos.length === 0}
    <div class="empty-state" transition:fade>
      <p>할 일이 없습니다.</p>
      <p>새로운 할 일을 추가해보세요! 🎯</p>
    </div>
  {:else}
    <div class="todo-list">
      {#each $filteredTodos as todo (todo.id)}
        <div animate:flip="{{ duration: 300 }}">
          <TodoItem 
            {todo}
            on:update={handleUpdateTodo}
            on:delete={handleDeleteTodo}
          />
        </div>
      {/each}
    </div>
  {/if}
</div>

<!-- 알림 메시지 -->
{#if $notifications.length > 0}
  <div class="notifications">
    {#each $notifications as notification (notification.id)}
      <div 
        class="notification notification-{notification.type}"
        transition:fade="{{ duration: 200 }}"
      >
        {notification.message}
      </div>
    {/each}
  </div>
{/if}

<style>
  .page {
    max-width: 800px;
    margin: 0 auto;
  }
  
  h1 {
    text-align: center;
    color: var(--primary);
    margin-bottom: 2rem;
  }
  
  .loading {
    text-align: center;
    padding: 2rem;
  }
  
  .spinner {
    width: 2rem;
    height: 2rem;
    border: 2px solid var(--border);
    border-top: 2px solid var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 1rem;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  .empty-state {
    text-align: center;
    padding: 3rem;
    color: var(--text-light);
  }
  
  .todo-list {
    margin-top: 1rem;
  }
  
  .notifications {
    position: fixed;
    top: 1rem;
    right: 1rem;
    z-index: 1000;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .notification {
    padding: 1rem;
    border-radius: 0.5rem;
    color: white;
    font-weight: 500;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }
  
  .notification-success {
    background: var(--success);
  }
  
  .notification-error {
    background: var(--error);
  }
  
  .notification-info {
    background: var(--primary);
  }
</style>