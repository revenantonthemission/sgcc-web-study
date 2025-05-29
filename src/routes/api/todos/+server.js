import { json } from '@sveltejs/kit';

// 메모리에 저장할 할 일 목록 (실제로는 데이터베이스 사용)
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

let nextId = 3;

/** @type {import('./$types').RequestHandler} */
export async function GET() {
  // 실제로는 데이터베이스에서 조회
  return json(todos);
}

/** @type {import('./$types').RequestHandler} */
export async function POST({ request }) {
  const newTodo = await request.json();
  
  const todo = {
    id: nextId++,
    ...newTodo,
    createdAt: new Date().toISOString()
  };
  
  todos.push(todo);
  
  return json(todo, { status: 201 });
}