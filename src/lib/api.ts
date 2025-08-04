import type { Memo } from './types';

const API_BASE_URL = 'http://localhost:8000';

export async function getMemos(): Promise<Memo[]> {
    const response = await fetch(`${API_BASE_URL}/memos/`);
    if (!response.ok) {
        throw new Error(`Failed to fetch memos: ${response.statusText}`);
    }
    return response.json();
}

export async function getMemo(id: number): Promise<Memo> {
    const response = await fetch(`${API_BASE_URL}/memos/${id}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch memo: ${response.statusText}`);
    }
    return response.json();
}

export async function createMemo(memo: { title: string; content: string }): Promise<Memo> {
    const response = await fetch(`${API_BASE_URL}/memos/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(memo),
    });
    if (!response.ok) {
        throw new Error(`Failed to create memo: ${response.statusText}`);
    }
    return response.json();
}

export async function updateMemo(id: number, memo: { title?: string; content?: string }): Promise<Memo> {
    const response = await fetch(`${API_BASE_URL}/memos/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(memo),
    });
    if (!response.ok) {
        throw new Error(`Failed to update memo: ${response.statusText}`);
    }
    return response.json();
}

export async function deleteMemo(id: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/memos/${id}`, {
        method: 'DELETE',
    });
    if (!response.ok) {
        throw new Error(`Failed to delete memo: ${response.statusText}`);
    }
}

export async function searchMemos(query: string): Promise<Memo[]> {
    const response = await fetch(`${API_BASE_URL}/memos/search/?q=${encodeURIComponent(query)}`);
    if (!response.ok) {
        throw new Error(`Failed to search memos: ${response.statusText}`);
    }
    return response.json();
}