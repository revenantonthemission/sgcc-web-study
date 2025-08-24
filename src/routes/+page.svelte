<script lang="ts">
    import MemoCard from '$lib/components/MemoCard.svelte';
    import MemoPlus from '$lib/components/MemoPlus.svelte';
    import type { Memo } from '$lib/types.ts';

    let { data } = $props();
    let selectedSort = $state('updated');

    const sortedMemos: Memo[] = $derived.by(() => {
        const originalMemos = [...data.memos];
        
        switch (selectedSort) {
            case 'newest':
                return originalMemos.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
            
            case 'name':
                return originalMemos.sort((a, b) => a.title.localeCompare(b.title));
            
            case 'updated':
                return originalMemos.sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime());

            default:
                return originalMemos.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
        }
    });
</script>

<div class="p-4">
  <label for="sort-select" class="mr-2 font-bold text-[#200F4C]">정렬 기준:</label>
  <select 
    bind:value={selectedSort} 
    id="sort-select" 
    class="p-2 rounded-md bg-[#200F4C] text-[#FFF3DF] focus:outline-none"
  >
    <option value="updated">업데이트순 (최신)</option>
    
    <option value="newest">만든순 (오래된 순)</option>
    
    <option value="name">이름순</option>
  </select>
</div>

<div class="columns-1 sm:columns-2 md:columns-3 lg:columns-4 xl:columns-5 2xl:columns-6 bg-[#FFF3DF]">
    {#each sortedMemos as memo (memo.id)}
        {#if memo.id % 2 == 0}
            <MemoCard memo={memo} memoColor="#200F4C"/>
        {:else}
            <MemoCard memo={memo} memoColor="#22949F"/>
        {/if}
    {/each}
    <MemoPlus />
</div>