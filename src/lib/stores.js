import { writable, derived } from 'svelte/store';
import { browser } from '$app/environment';

// 할 일 스토어
export const todos = writable([]);

// 필터 스토어
export const filter = writable('all');

// 테마 스토어
function createTheme() {
  const { subscribe, set } = writable('light');
  
  return {
    subscribe,
    toggle: () => {
      set(get(theme) === 'light' ? 'dark' : 'light');
    },
    set
  };
}

export const theme = createTheme();

// 필터된 할 일 목록
export const filteredTodos = derived(
  [todos, filter],
  ([$todos, $filter]) => {
    switch ($filter) {
      case 'completed':
        return $todos.filter(todo => todo.completed);
      case 'pending':
        return $todos.filter(todo => !todo.completed);
      default:
        return $todos;
    }
  }
);

// 통계 정보
export const stats = derived(todos, ($todos) => ({
  total: $todos.length,
  completed: $todos.filter(t => t.completed).length,
  pending: $todos.filter(t => !t.completed).length
}));

// 로딩 상태
export const loading = writable(false);

// 알림 메시지
export const notifications = writable([]);