import camelcaseKeys from "camelcase-keys";
import { PUBLIC_API_BASE_URL } from "$env/static/public";
import type { Memo } from "$lib/types";

const BASE_URL = PUBLIC_API_BASE_URL;

async function apiFetch<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
	const defaultHeaders = {
		"Content-Type": "application/json"
	};

	const response = await fetch(`${BASE_URL}${endpoint}`, {
		...options,
		headers: {
			...defaultHeaders,
			...options.headers
		}
	});

	if (!response.ok) {
		throw new Error(`Request failed: ${response.status} ${response.statusText}`);
	}

	if (response.status === 204) {
		return null as T;
	}

	const data = await response.json();

	return camelcaseKeys(data, { deep: true }) as T;
}

export function createMemo(title: string, content: string): Promise<Memo> {
	return apiFetch<Memo>("/memos/", {
		method: "POST",
		body: JSON.stringify({ title, content })
	});
}

export function getMemos(): Promise<Memo[]> {
	return apiFetch<Memo[]>("/memos/");
}

export function getMemoById(id: number): Promise<Memo> {
	return apiFetch<Memo>(`/memos/${id}`);
}

export function updateMemo(id: number, title: string, content: string): Promise<Memo> {
	return apiFetch<Memo>(`/memos/${id}`, {
		method: "PUT",
		body: JSON.stringify({ title, content })
	});
}

export function deleteMemo(id: number): Promise<void> {
	return apiFetch<void>(`/memos/${id}`, {
		method: "DELETE"
	});
}

export function searchMemos(query: string): Promise<Memo[]> {
	const encodedQuery = encodeURIComponent(query);
	return apiFetch<Memo[]>(`/memos/search/?q=${encodedQuery}`);
}