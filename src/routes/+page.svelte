<script lang="ts">
    import MemoCard from "$lib/components/MemoCard.svelte";
    import MemoPlus from "$lib/components/MemoPlus.svelte";
    import type { Memo } from "$lib/types";
    import type { PageData } from "./$types";

    export let data: PageData;

    let memos = data.memos;
    $: memos = data.memos;
</script>

<div class="columns-1 sm:columns-2 md:columns-3 lg:columns-4 xl:columns-5 2xl:columns-6 bg-[#FFF3DF]">
    {#each [...memos].reverse() as memo (memo.id)}
        {#if memo.id % 2 == 0}
            <MemoCard memo={memo} memoColor="#200F4C"/>
        {:else}
            <MemoCard memo={memo} memoColor="#22949F"/>
        {/if}
    {/each}
    <MemoPlus />
</div>