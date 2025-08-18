import type { Memo } from './types';
import { browser } from '$app/environment';

// Use different base URLs for server vs client
const API_BASE_URL = browser ? '' : 'http://127.0.0.1:8000';

export async function getMemos(): Promise<Memo[]> {
    try {
        const response = await fetch(`${API_BASE_URL}/memos/`);
        if (!response.ok) {
            throw new Error(`Failed to fetch memos: ${response.statusText}`);
        }
        
        const text = await response.text();
        if (!text || text.trim().startsWith('<!DOCTYPE') || text.trim().startsWith('<html')) {
            // Server returned HTML instead of JSON, likely means API server is not running
            console.warn('API server not available, returning empty memo list');
            return [];
        }
        
        return JSON.parse(text);
    } catch (error) {
        console.error('Error fetching memos:', error);
        // Return empty array instead of throwing error to prevent app crash
        return [];
    }
}

export async function getMemo(id: number): Promise<Memo> {
    try {
        const response = await fetch(`${API_BASE_URL}/memos/${id}`);
        if (!response.ok) {
            throw new Error(`Failed to fetch memo: ${response.statusText}`);
        }
        
        const text = await response.text();
        if (!text || text.trim().startsWith('<!DOCTYPE') || text.trim().startsWith('<html')) {
            throw new Error('API server not available - cannot fetch memo');
        }
        
        return JSON.parse(text);
    } catch (error) {
        console.error('Error fetching memo:', error);
        throw error;
    }
}

export async function createMemo(memo: { title: string; content: string }): Promise<Memo> {
    try {
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
        
        const text = await response.text();
        if (!text || text.trim().startsWith('<!DOCTYPE') || text.trim().startsWith('<html')) {
            throw new Error('API server not available - cannot create memo');
        }
        
        return JSON.parse(text);
    } catch (error) {
        console.error('Error creating memo:', error);
        throw error;
    }
}

export async function updateMemo(id: number, memo: { title?: string; content?: string }): Promise<Memo> {
    try {
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
        
        const text = await response.text();
        if (!text || text.trim().startsWith('<!DOCTYPE') || text.trim().startsWith('<html')) {
            throw new Error('API server not available - cannot update memo');
        }
        
        return JSON.parse(text);
    } catch (error) {
        console.error('Error updating memo:', error);
        throw error;
    }
}

export async function deleteMemo(id: number): Promise<void> {
    try {
        const response = await fetch(`${API_BASE_URL}/memos/${id}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error(`Failed to delete memo: ${response.statusText}`);
        }
        
        // DELETE typically returns empty response, so just check if response is HTML
        const text = await response.text();
        if (text && (text.trim().startsWith('<!DOCTYPE') || text.trim().startsWith('<html'))) {
            throw new Error('API server not available - cannot delete memo');
        }
    } catch (error) {
        console.error('Error deleting memo:', error);
        throw error;
    }
}

export async function searchMemos(query: string): Promise<Memo[]> {
    try {
        const response = await fetch(`${API_BASE_URL}/memos/search/?q=${encodeURIComponent(query)}`);
        if (!response.ok) {
            throw new Error(`Failed to search memos: ${response.statusText}`);
        }
        
        const text = await response.text();
        if (!text || text.trim().startsWith('<!DOCTYPE') || text.trim().startsWith('<html')) {
            console.warn('API server not available, returning empty search results');
            return [];
        }
        
        return JSON.parse(text);
    } catch (error) {
        console.error('Error searching memos:', error);
        return [];
    }
}