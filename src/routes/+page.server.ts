import type { PageServerLoad } from './$types';
import { getMemos } from '$lib/api';
import type { Memo } from '$lib/types';

export const load: PageServerLoad = async () => {
	try {
        let memos = await getMemos();
		return { memos: memos };
	} catch (error) {
		return { memos: [] };
    }
};