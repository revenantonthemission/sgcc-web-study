import { json, error } from '@sveltejs/kit';

// 실제로는 데이터베이스에서 관리
let todos = [
  {
    id: 1,
    text: 'SvelteKit 학습하기',
    completed: false,
    priority: 'high',
    category: '학습',
    createdAt: new Date().toISOString()
  },
  {
    id: 2,
    text: '프로젝트 계획 세우기',
    completed: true,
    priority: 'medium',
    category: '업무',
    createdAt: new Date(Date.now() - 86400000).toISOString()
  }
];

/** @type {import('./$types').RequestHandler} */
export async function PATCH({ params, request }) {
  const id = parseInt(params.id);
  const updates = await request.json();
  
  const todoIndex = todos.findIndex(todo => todo.id === id);
  
  if (todoIndex === -1) {
    throw error(404, 'Todo not found');
  }
  
  todos[todoIndex] = { ...todos[todoIndex], ...updates };
  
  return json(todos[todoIndex]);
}

/** @type {import('./$types').RequestHandler} */
export async function DELETE({ params }) {
  const id = parseInt(params.id);
  
  const todoIndex = todos.findIndex(todo => todo.id === id);
  
  if (todoIndex === -1) {
    throw error(404, 'Todo not found');
  }
  
  todos.splice(todoIndex, 1);
  
  return json({ success: true });
}